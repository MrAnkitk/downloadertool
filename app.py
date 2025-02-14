import streamlit as st
import yt_dlp
import os
import time
import re

# Ensure downloads directory exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Track download count
if "download_count" not in st.session_state:
    st.session_state.download_count = 0

def sanitize_filename(title):
    """Sanitize filename to remove special characters."""
    return re.sub(r'[\\/*?:"<>|]', "", title)

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
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s-%(id)s.%(ext)s',
        'noplaylist': True,  # Prevent downloading playlists
        'quiet': True,  # Hide console logs
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if "title" not in info or "ext" not in info:
                return None, "Error: Invalid video metadata."

            sanitized_title = sanitize_filename(info["title"])
            file_extension = info["ext"]
            file_path = f"{DOWNLOAD_FOLDER}/{sanitized_title}-{info['id']}.{file_extension}"
            
            return file_path, None  # No error
    except Exception as e:
        return None, str(e)

st.title("📥 Video & Audio Downloader - YouTube & Instagram")
st.write("Paste the video URL below and click 'Download'.")

# Platform selection
platform = st.selectbox("Select Platform", ["YouTube", "Instagram"])

# Media type selection
media_type = st.radio("Select Media Type", ["Video", "Audio Only"])

# Video quality selection
quality_options = ["1080p", "720p", "480p", "360p", "240p", "144p"]
if media_type == "Audio Only":
    quality_options = ["Audio Only"]

quality = st.selectbox("Select Quality", quality_options)

url = st.text_input("Enter Video URL")
if st.button("Download"):
    if url:
        with st.spinner("Downloading... Please wait."):
            file_path, error = download_media(url, quality)

            if file_path and os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    st.download_button(label="Download", data=file, file_name=os.path.basename(file_path))
                st.success("✅ Download complete! Click above to save the file.")

                # Track download count
                st.session_state.download_count += 1

                # Show popup on second download
                if st.session_state.download_count >= 2:
                    time.sleep(2)
                    with st.expander("🎉 Download Successful! Click to Support 🎉", expanded=True):
                        st.markdown("## 🤑 *Ek Cup Chai Toh Banta Hai!* ☕")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Haan Bhai! Support Kar Raha Hoon!"):
                                st.markdown("[**Donate via UPI (Click to Pay)**](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")
                                st.success("❤️ Thank you for your support! ❤️")

                        with col2:
                            if st.button("❌ Nahi Bhai, Paisa Nahi Hai"):
                                st.warning("Koi nahi! Aage kabhi support kar dena! 😊")
            else:
                st.error(f"🚨 {error if error else 'Unknown error occurred.'}")
    else:
        st.warning("⚠️ Please enter a valid URL.")

# Donation Section
st.markdown("---")
st.header("💖 Support the Developer")

st.markdown(
    "Toh doston, chinta mat karo, **life ka UPI PIN strong rakho, relationships ka OTP safe rakho, aur success ka QR Code scan karne ki koshish karte raho!** 😆🔥\n\n"
)

# UPI QR Code Image
st.image("qrcode.jpg", caption="Scan to Donate via UPI", width=150)

# Payment Link
st.write("[Donate via UPI (Click to Pay)](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")

st.write("Developed by Ankit Shrivastava")
