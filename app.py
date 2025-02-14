import streamlit as st
import yt_dlp
import os

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

def download_media(url, quality, platform, media_type):
    format_map = {
        "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "480p": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "360p": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "240p": "bestvideo[height<=240][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "144p": "bestvideo[height<=144][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "Audio Only": "bestaudio[ext=m4a]/bestaudio"
    }

    extra_args = {}
    if platform == "Instagram Reels":
        extra_args = {
            'referer': 'https://www.instagram.com/',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'extractor_args': {'instagram': ''},
            'merge_output_format': None  # Disable merging
        }

    options = {
        'format': format_map.get(quality, 'best[ext=mp4]'),
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [],  # Disable ffmpeg usage
        **extra_args
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            if os.path.exists(file_path):
                return file_path
            else:
                return None
    except Exception as e:
        return str(e)

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
            file_path = download_media(url, quality, platform, media_type)
            if file_path and os.path.exists(file_path):
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

st.markdown("---")
st.header("💖 Support the Developer")

st.image("qrcode.jpg", caption="Scan to Donate via UPI", width=100)
st.write("[Donate via UPI (Click to Pay)](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")

st.write("Developed by Ankit Shrivastava")
