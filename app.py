import streamlit as st
import yt_dlp
import os

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

def download_media(url, quality, platform):
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
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9'
        }
    }
    
    # Instagram reels ke liye login cookies ka support
    if platform == "Instagram Reels":
        options['cookies'] = 'cookies.txt'  # Instagram ke login session ka cookies file

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            absolute_path = os.path.abspath(file_path)
            
            # Check if file exists
            if os.path.exists(absolute_path):
                return absolute_path
            else:
                st.error("⚠️ Error: File was not saved correctly. Try again!")
                return None
    except Exception as e:
        st.error(f"⚠️ Download Failed: {str(e)}")
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
            file_path = download_media(url, quality, platform)
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

st.markdown("---")
st.header("💖 Support the Developer")
st.image("qrcode.jpg", caption="Scan to Donate via UPI", width=100)
st.write("[Donate via UPI (Click to Pay)](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")

st.write("Developed by Ankit Shrivastava")
