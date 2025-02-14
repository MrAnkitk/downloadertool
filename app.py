import streamlit as st
import yt_dlp
import os

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

def download_media(url, quality, platform, media_type):
    format_map = {
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "360p": "bestvideo[height<=360]+bestaudio/best",
        "240p": "bestvideo[height<=240]+bestaudio/best",
        "144p": "bestvideo[height<=144]+bestaudio/best",
        "Audio Only": "bestaudio/best"  # Audio only
    }
    
    options = {
        'format': format_map.get(quality, 'best'),
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            return file_path
    except Exception as e:
        return str(e)

st.title("📥 Video & Audio Downloader - Instagram & YouTube")
st.write("Paste the video URL below and click 'Download'")

# Platform selection
platform = st.selectbox("Select Platform", ["YouTube Video", "Instagram Reels"])

# Media type selection (Video or Audio)
media_type = st.radio("Select Media Type", ["Video", "Audio Only"])

# Video quality selection (Only for Video)
quality_options = ["1080p", "720p", "480p", "360p", "240p", "144p"]
if media_type == "Audio Only":
    quality_options = ["Audio Only"]

quality = st.selectbox("Select Quality", quality_options)

url = st.text_input("Enter Video URL")
if st.button("Download"):
    if url:
        with st.spinner("Downloading... Please wait."):
            file_path = download_media(url, quality, platform, media_type)
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    st.download_button(label="Download", data=file, file_name=os.path.basename(file_path))
                st.success("Download complete! Click above to save the file.")
            else:
                st.error(f"Error: {file_path}")  # Showing the error message
    else:
        st.warning("Please enter a valid URL")

st.write("Developed by Ankit Kumar")
