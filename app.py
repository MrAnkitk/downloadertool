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

st.title("\ud83d\udce5 Video & Audio Downloader")
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
                st.success("\u2705 Download Successful! Click below to save the file.")
            else:
                st.error("\u26a0\ufe0f Error: File not found. Please try again.")
    else:
        st.warning("Please enter a valid URL.")

# Show Download Button only if file exists
if st.session_state.download_completed and st.session_state.download_path:
    with open(st.session_state.download_path, "rb") as file:
        st.download_button(
            label="\ud83d\udce5 Click to Download",
            data=file,
            file_name=os.path.basename(st.session_state.download_path),
            mime="application/octet-stream"
        )

# If download completed, show popup
if st.session_state.download_completed:
    with st.expander("\ud83c\udf89 Download Successful! Click to Support \ud83c\udf89", expanded=True):
        st.markdown("## \ud83e\udd11 *Yaar! Ek Cup Chai Toh Banta Hai!* ☕")
        st.write("Yahhan, Dabate Hi Download Hota Hai")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("\u2705 Haan Bhai! Support Kar Raha Hoon!"):
                st.markdown("[**Donate via UPI (Click to Pay)**](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")
                st.success("❤️ Thank you for your support! ❤️")

        with col2:
            if st.button("\u274c Nahi Bhai, Abhi Paisa Nahi Hai"):
                st.warning("Koi nahi! Aage kabhi support kar dena! 😊")

st.markdown("---")
st.header("💖 Support the Developer")

st.markdown(
    "Toh doston, chinta mat karo, **life ka UPI PIN strong rakho, relationships ka OTP safe rakho, aur success ka QR Code scan karne ki koshish karte raho!** 😆🔥\n\n"
)
st.image("qrcode.jpg", caption="Scan to Donate via UPI", width=100)
st.write("[Donate via UPI (Click to Pay)](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")

st.write("Developed by Ankit Shrivastava")
