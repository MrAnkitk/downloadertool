import streamlit as st
import yt_dlp
import os
import time

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

# Session state to track downloads
if "download_completed" not in st.session_state:
    st.session_state.download_completed = False
if "download_path" not in st.session_state:
    st.session_state.download_path = None

def download_media(url, quality, platform, media_type):
    format_map = {
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "360p": "bestvideo[height<=360]+bestaudio/best",
        "240p": "bestvideo[height<=240]+bestaudio/best",
        "144p": "bestvideo[height<=144]+bestaudio/best",
        "Audio Only": "bestaudio/best"
    }
    
    options = {
        'format': format_map.get(quality, 'best'),
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            absolute_path = os.path.abspath(file_path)
            return absolute_path
    except Exception as e:
        return None

st.title("📥 Video & Audio Downloader")
st.write("Paste the video URL below and click 'Download'")

platform = st.selectbox("Select Platform", ["YouTube Video", "Instagram Reels"])
media_type = st.radio("Select Media Type", ["Video", "Audio Only"])
quality_options = ["1080p", "720p", "480p", "360p", "240p", "144p"]
if media_type == "Audio Only":
    quality_options = ["Audio Only"]
quality = st.selectbox("Select Quality", quality_options)

url = st.text_input("Enter Video URL")

if st.button("Download"):
    if url:
        with st.spinner("Downloading... Please wait."):
            file_path = download_media(url, quality, platform, media_type)
            if file_path and os.path.exists(file_path):
                st.session_state.download_path = file_path
                st.session_state.download_completed = True
                st.success("✅ Download Successful! Click below to save the file.")
            else:
                st.error("⚠️ Error: File not found. Please try again.")
    else:
        st.warning("Please enter a valid URL.")

# Show Download Button only if file exists
if st.session_state.download_completed and st.session_state.download_path:
    with open(st.session_state.download_path, "rb") as file:
        st.download_button(
            label="📥 Click to Download",
            data=file,
            file_name=os.path.basename(st.session_state.download_path),
            mime="application/octet-stream"
        )
