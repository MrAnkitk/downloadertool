# -*- coding: utf-8 -*-

import streamlit as st
import yt_dlp
import os
import time

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

# Session state to track downloads
if "download_completed" not in st.session_state:
    st.session_state.download_completed = False

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
        'format': format_map.get(quality, 'bestvideo+bestaudio/best'),
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,  # Sirf ek hi video download hogi, playlist nahi
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferredformat': 'mp4',  # Fix: preferedformat -> preferredformat
        }],
        'retries': 10,  # Agar download fail ho toh 10 baar retry karega
        'fragment_retries': 10,
        'socket_timeout': 30,
        'nopart': False,  # Agar ek part fail ho toh poora video fail na ho
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            st.write(f"Generated file path: {file_path}")  # Debugging output
            return file_path if os.path.exists(file_path) else None
    except Exception as e:
        return str(e)

# Streamlit UI
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
    if st.session_state.download_completed:
        st.success("\ud83c\udf89 Download already completed! Showing popup...")
    else:
        if url:
            with st.spinner("Downloading... Please wait."):
                file_path = download_media(url, quality, platform, media_type)
                if file_path and os.path.exists(file_path):
                    with open(file_path, "rb") as file:
                        st.download_button(label="Save Media", data=file, file_name=os.path.basename(file_path))

                    st.success("Download complete! Click above to save the file.")

                    # Mark download as completed
                    st.session_state.download_completed = True

                    # Wait for a moment before showing popup
                    time.sleep(2)
                    
                    st.success("\ud83c\udf89 Download Successful! Showing popup...")
                else:
                    st.error("Download failed. Please check the URL or try again.")
        else:
            st.warning("Please enter a valid URL")

# If download completed, show popup
if st.session_state.download_completed:
    with st.expander("\ud83c\udf89 Download Successful! Click to Support \ud83c\udf89", expanded=True):
        st.markdown("## \ud83e\udd11 *Yaar! Ek Cup Chai Toh Banta Hai!* ☕")
        st.write("Yahhan, Dabate Hi Download Hota Hai")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Haan Bhai! Support Kar Raha Hoon!"):
                st.markdown("[**Donate via UPI (Click to Pay)**](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")
                st.success("❤️ Thank you for your support! ❤️")

        with col2:
            if st.button("❌ Nahi Bhai, Abhi Paisa Nahi Hai"):
                st.warning("Koi nahi! Aage kabhi support kar dena! 😊")

st.markdown("---")
st.header("💖 Support the Developer")

st.markdown(
    "Toh doston, chinta mat karo, **life ka UPI PIN strong rakho, relationships ka OTP safe rakho, aur success ka QR Code scan karne ki koshish karte raho!** 😆🔥\n\n"
)
st.image("qrcode.jpg", caption="Scan to Donate via UPI", width=150)
st.write("[Donate via UPI (Click to Pay)](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")

st.write("Developed by Ankit Shrivastava")
