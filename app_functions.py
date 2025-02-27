import io
import os
import base64
import tempfile
from generate_gif import extract_gpx_points, save_map_images, create_gif

def process_files(derive_file, trajectoire_files):
    # Create temporary directory for files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded files to temporary directory
        derive_path = os.path.join(temp_dir, derive_file.name)
        with open(derive_path, 'wb') as f:
            f.write(derive_file.getbuffer())
        
        trajectoire_paths = []
        for file in trajectoire_files:
            path = os.path.join(temp_dir, file.name)
            with open(path, 'wb') as f:
                f.write(file.getbuffer())
            trajectoire_paths.append(path)

        # Process files
        derive_points = extract_gpx_points(derive_path)
        trajectoire_points_list = [extract_gpx_points(path) for path in trajectoire_paths]

    start_time = min(point[2] for point in derive_points if point[2] is not None)
    end_time = max(max(point[2] for point in points if point[2] is not None) for points in trajectoire_points_list)

    images = save_map_images(derive_points, trajectoire_points_list, start_time, end_time, trajectoire_paths)
    gif_bytes = create_gif(images)

    return gif_bytes, trajectoire_paths
