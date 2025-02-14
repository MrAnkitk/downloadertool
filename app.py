import streamlit as st
import yt_dlp
import os
import time

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

# Session state to track downloads
if "download_completed" not in st.session_state:
    st.session_state.download_completed = False

def sanitize_filename(filename):
    """Remove special characters to ensure valid filenames."""
    return "".join(c for c in filename if c.isalnum() or c in (" ", ".", "_")).rstrip()

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
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Use ID instead of title
        'noplaylist': True
    }
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            file_path = sanitize_filename(file_path)  # Clean file name
            return file_path if os.path.exists(file_path) else None
    except Exception as e:
        return str(e)

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
                with open(file_path, "rb") as file:
                    st.download_button(label="Download", data=file, file_name=os.path.basename(file_path))
                
                st.success("✅ Download complete! Click above to save the file.")
                st.session_state.download_completed = True  # Mark as completed
                
                time.sleep(2)
                st.success("🎉 Download Successful!")
            else:
                st.error("⚠️ Error: File not found. Please try again.")
    else:
        st.warning("⚠️ Please enter a valid URL.")

if st.session_state.download_completed:
    with st.expander("🎉 Download Successful! Click to Support 🎉", expanded=True):
        st.markdown("## 🤑 *Yaar! Ek Cup Chai Toh Banta Hai!* ☕")
        st.write("Yahaan, Dabate Hi Download Hota Hai")

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
st.image("qrcode.jpg", caption="Scan to Donate via UPI", width=100)
st.write("[Donate via UPI (Click to Pay)](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")

st.write("Developed by Ankit Shrivastava")
