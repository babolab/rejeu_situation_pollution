import streamlit as st
import io
import os
import base64
from app_functions import process_files
from datetime import datetime

def main():
    st.title("Simulation de Dérive et Trajectoires de Navires")

    # Upload files
    derive_file = st.file_uploader("Télécharger le fichier de dérive", type=["gpx"])
    trajectoire_files = st.file_uploader("Télécharger les fichiers de trajectoire", type=["gpx"], accept_multiple_files=True)

    colors = ['red', 'green', 'blue', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen']

    if st.button("Lancer la simulation"):
        if derive_file and trajectoire_files:
            gif_bytes, trajectoire_paths = process_files(derive_file, trajectoire_files)

            # Display legend
            legend_html = "<div style='font-size: 12pt;'>Légende:</div><ul>"
            for i, path in enumerate(trajectoire_paths):
                color = colors[i % len(colors)]
                filename = os.path.basename(path)[:20]
                legend_html += f"<li style='color: {color};'>{filename}</li>"
            legend_html += "</ul>"
            st.markdown(legend_html, unsafe_allow_html=True)

            st.success("GIF créé avec succès")
            # Display GIF with pause functionality
            st.markdown(
                f"""
                <img src="data:image/gif;base64,{base64.b64encode(gif_bytes).decode()}" style="width:100%;" id="gif" onmouseover="this.style.animationPlayState='running'" onmouseout="this.style.animationPlayState='paused'">
                <button onclick="document.getElementById('gif').style.animationPlayState='paused';">Pause</button>
                <button onclick="document.getElementById('gif').style.animationPlayState='running';">Play</button>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()
