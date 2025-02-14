import streamlit as st
import yt_dlp
import os
import instaloader

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

# Function to download YouTube/Facebook videos using yt-dlp
def download_yt_fb(url, quality):
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
            
            if os.path.exists(absolute_path):
                return absolute_path
            else:
                st.error("⚠️ Error: File was not saved correctly. Try again!")
                return None
    except Exception as e:
        st.error(f"⚠️ Download Failed: {str(e)}")
        return None

# Function to download Instagram Reels using instaloader
def download_instagram_reel(url):
    try:
        L = instaloader.Instaloader(dirname_pattern="downloads")
        post_shortcode = url.split("/")[-2]  # Extract shortcode from URL
        L.download_post(instaloader.Post.from_shortcode(L.context, post_shortcode), target="downloads")
        
        # Find the downloaded file
        for file in os.listdir("downloads"):
            if file.endswith(".mp4"):
                return os.path.abspath(os.path.join("downloads", file))
        
        st.error("⚠️ Error: File was not saved correctly. Try again!")
        return None
    except Exception as e:
        st.error(f"⚠️ Instagram Download Failed: {str(e)}")
        return None

st.title("📥 Video & Audio Downloader")
st.write("Paste the video URL below and click 'Download'")

platform = st.selectbox("Select Platform", ["YouTube Video", "Instagram Reels", "Facebook Reels"])
media_type = st.radio("Select Media Type", ["Video", "Audio Only"])

quality_options = ["1080p", "720p", "480p", "360p", "240p", "144p"]
if media_type == "Audio Only":
    quality_options = ["Audio Only"]
quality = st.selectbox("Select Quality", quality_options)

url = st.text_input("Enter Video URL")

if st.button("Download"):
    if url:
        with st.spinner("Downloading... Please wait."):
            if platform in ["YouTube Video", "Facebook Reels"]:
                file_path = download_yt_fb(url, quality)
            elif platform == "Instagram Reels":
                file_path = download_instagram_reel(url)
            else:
                file_path = None

            if file_path:
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="📥 Save Media",
                        data=file,
                        file_name=os.path.basename(file_path),
                        mime="application/octet-stream"
                    )
                    st.success("✅ Download Successful!")
            else:
                st.error("⚠️ Download failed. Please try again!")
    else:
        st.warning("Please enter a valid URL.")
