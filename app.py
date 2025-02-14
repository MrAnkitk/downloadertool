import streamlit as st
import yt_dlp
import os

# Ensure downloads directory exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Session state to track downloads
if "download_completed" not in st.session_state:
    st.session_state.download_completed = False
if "download_path" not in st.session_state:
    st.session_state.download_path = None

def download_media(url, quality):
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
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,  # Hide unnecessary logs
    }
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
            absolute_path = os.path.abspath(file_name)

            # Check if file exists
            if os.path.exists(absolute_path):
                return absolute_path
            else:
                st.error(f"⚠️ File not found: {absolute_path}")
                return None
    except Exception as e:
        st.error(f"❌ Download Failed: {str(e)}")
        return None

st.title("📥 Video & Audio Downloader")

url = st.text_input("Enter Video URL")
quality = st.selectbox("Select Quality", ["1080p", "720p", "480p", "360p", "240p", "144p", "Audio Only"])

if st.button("Download"):
    if url:
        with st.spinner("Downloading... Please wait."):
            file_path = download_media(url, quality)
            
            if file_path:
                st.session_state.download_path = file_path
                st.session_state.download_completed = True
                st.success("✅ Download Successful! Click below to save the file.")
            else:
                st.error("⚠️ Error: File not found. Please try again.")
    else:
        st.warning("Please enter a valid URL.")

# Show Download Button if file exists
if st.session_state.download_completed and st.session_state.download_path:
    with open(st.session_state.download_path, "rb") as file:
        st.download_button(
            label="📥 Click to Download",
            data=file,
            file_name=os.path.basename(st.session_state.download_path),
            mime="application/octet-stream"
        )
