import gpxpy
import gpxpy.gpx
import folium
from datetime import datetime, timedelta
import imageio
from PIL import Image
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def extract_gpx_points(file_path):
    points = []
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude, point.time))
        for waypoint in gpx.waypoints:
            points.append((waypoint.latitude, waypoint.longitude, waypoint.time))
    return points

def create_map(derive_points, trajectoire_points_list, current_time, trajectoire_filenames):
    # Calculate bounds with a 10 nautical mile buffer
    lats = [point[0] for point in derive_points]
    lons = [point[1] for point in derive_points]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)

    # Convert nautical miles to degrees (approximation)
    nautical_mile_to_degree = 10 / 60.0

    # Apply buffer
    min_lat -= nautical_mile_to_degree
    max_lat += nautical_mile_to_degree
    min_lon -= nautical_mile_to_degree
    max_lon += nautical_mile_to_degree

    # Calculate center
    center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
    map_ = folium.Map(location=center, zoom_start=14, tiles='OpenStreetMap')
    map_.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

    # Filter derive points for the current time
    current_derive_points = [(lat, lon) for lat, lon, time in derive_points if time and time == current_time]
    for lat, lon in current_derive_points:
        folium.CircleMarker(location=[lat, lon], radius=5, color='blue', fill=True).add_to(map_)

    colors = ['red', 'green', 'blue', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen']
    
    for i, (trajectoire_points, trajectoire_filename) in enumerate(zip(trajectoire_points_list, trajectoire_filenames)):
        # Filter trajectoire points for the current time within 1 hour
        current_trajectoire_points = [(lat, lon) for lat, lon, time in trajectoire_points if time and abs((time - current_time).total_seconds()) <= 3600]
        
        # Add the current trajectoire points
        for lat, lon in current_trajectoire_points:
            folium.CircleMarker(location=[lat, lon], radius=5, color=colors[i % len(colors)], fill=True).add_to(map_)

        # Add legend with the ship trajectory filename at the bottom left
        folium.map.Marker(
            location=[min_lat - 0.06 * i, min_lon - 0.1],  # Offset each label more vertically and to the left
            icon=folium.DivIcon(
                icon_size=(200, 36),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 10pt; color: {colors[i % len(colors)]};">{os.path.basename(trajectoire_filename)[:20]}</div>',
            )
        ).add_to(map_)

    # Add current time at the top right
    folium.map.Marker(
        location=[max_lat, max_lon],
        icon=folium.DivIcon(
            icon_size=(200, 36),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12pt; color: black;">{current_time.strftime("%Y-%m-%d %H:%M:%S")}</div>',
        )
    ).add_to(map_)

    folium.map.LayerControl('topright', collapsed=False).add_to(map_)

    return map_

def save_map_images(derive_points, trajectoire_points_list, start_time, end_time, trajectoire_files):
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    images = []
    current_time = start_time
    while current_time <= end_time:
        map_ = create_map(derive_points, trajectoire_points_list, current_time, [os.path.basename(f) for f in trajectoire_files])
        image_path = f"map_{current_time.strftime('%Y%m%d_%H%M%S')}.png"
        map_.save('temp_map.html')
        driver.get('file://' + os.path.abspath('temp_map.html'))
        driver.set_window_size(800, 600)
        driver.save_screenshot(image_path)
        images.append(image_path)
        current_time += timedelta(hours=1)
    driver.quit()
    return images

def create_gif(images):
    frames = [Image.open(image) for image in images]
    gif_path = "rejeu.gif"
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=500, loop=0)
    return gif_path

def main():
    derive_file = next((os.path.join('mothy', f) for f in os.listdir('mothy') if f.endswith('.gpx')), None)
    if not derive_file:
        raise FileNotFoundError("No drift file found in the 'mothy' directory.")
    trajectoire_files = [os.path.join('trajectoires', f) for f in os.listdir('trajectoires') if f.endswith('.gpx')]

    derive_points = extract_gpx_points(derive_file)
    trajectoire_points_list = [extract_gpx_points(f) for f in trajectoire_files]

    start_time = min(point[2] for point in derive_points if point[2] is not None)
    end_time = max(max(point[2] for point in points if point[2] is not None) for points in trajectoire_points_list)

    images = save_map_images(derive_points, trajectoire_points_list, start_time, end_time, trajectoire_files)
    gif_path = create_gif(images)

    print(f"GIF created at {gif_path}")

if __name__ == "__main__":
    main()
