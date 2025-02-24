import streamlit as st
import os
import base64
from generate_gif import extract_gpx_points, save_map_images, create_gif
from datetime import datetime

def main():
    st.title("Simulation de Dérive et Trajectoires de Navires")

    # Upload files
    derive_file = st.file_uploader("Télécharger le fichier de dérive", type=["gpx"])
    trajectoire_files = st.file_uploader("Télécharger les fichiers de trajectoire de navires", type=["gpx"], accept_multiple_files=True)

    colors = ['red', 'green', 'blue', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen']

    if st.button("Lancer la simulation"):
        if derive_file and trajectoire_files:
            # Save uploaded files to disk
            derive_path = os.path.join("mothy", derive_file.name)
            with open(derive_path, "wb") as f:
                f.write(derive_file.getbuffer())

            trajectoire_paths = []
            for file in trajectoire_files:
                path = os.path.join("trajectoires", file.name)
                with open(path, "wb") as f:
                    f.write(file.getbuffer())
                trajectoire_paths.append(path)

            # Process files
            derive_points = extract_gpx_points(derive_path)
            trajectoire_points_list = [extract_gpx_points(path) for path in trajectoire_paths]

            start_time = min(point[2] for point in derive_points if point[2] is not None)
            end_time = max(max(point[2] for point in points if point[2] is not None) for points in trajectoire_points_list)

            images = save_map_images(derive_points, trajectoire_points_list, start_time, end_time, trajectoire_paths)
            gif_path = create_gif(images)

            # Display legend
            legend_html = "<div style='font-size: 12pt;'>Légende:</div><ul>"
            for i, path in enumerate(trajectoire_paths):
                color = colors[i % len(colors)]
                filename = os.path.basename(path)[:20]
                legend_html += f"<li style='color: {color};'>{filename}</li>"
            legend_html += "</ul>"
            st.markdown(legend_html, unsafe_allow_html=True)

            st.success(f"GIF créé à {gif_path}")
            # Display GIF with pause functionality
            st.markdown(
                f"""
                <img src="data:image/gif;base64,{base64.b64encode(open(gif_path, "rb").read()).decode()}" style="width:100%;" id="gif" onmouseover="this.style.animationPlayState='running'" onmouseout="this.style.animationPlayState='paused'">
                <button onclick="document.getElementById('gif').style.animationPlayState='paused';">Pause</button>
                <button onclick="document.getElementById('gif').style.animationPlayState='running';">Play</button>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()
