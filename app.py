import streamlit as st
import yt_dlp
import os
import time

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

# Track download count
download_count = st.session_state.get("download_count", 0)

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
            return file_path
    except Exception as e:
        return str(e)

st.title("📥 Video & Audio Downloader - Instagram & YouTube")
st.write("Paste the video URL below and click 'Download'")

# Platform selection
platform = st.selectbox("Select Platform", ["YouTube Video", "Instagram Reels"])

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
            file_path = download_media(url, quality, platform, media_type)
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    st.download_button(label="Download", data=file, file_name=os.path.basename(file_path))
                st.success("Download complete! Click above to save the file.")
                
                # Increment download count
                st.session_state.download_count = st.session_state.get("download_count", 0) + 1
                
                # Show popup on second download
                if st.session_state.download_count >= 2:
                    time.sleep(2)
                    with st.expander("🎉 Download Successful! Click to Support 🎉", expanded=True):
                        st.markdown("## 🤑 *Yaar! Ek Cup Chai Toh Banta Hai!* ☕")
                        st.write("Agar ye tool useful laga, toh ek chhoti si chai donate karke support karein!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Haan Bhai! Support Kar Raha Hoon!"):
                                st.markdown("[Donate via UPI](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")
                                st.success("❤️ Thank you for your support! ❤️")
                        
                        with col2:
                            if st.button("❌ Nahi Bhai, Paisa Abhi Pocket Me Nahi Hai"):
                                st.warning("Koi nahi! Aage kabhi support kar dena! 😊")
            else:
                st.error(f"Error: {file_path}")
    else:
        st.warning("Please enter a valid URL")

# Donate Section
st.markdown("---")
st.header("💖 Support the Developer")

st.markdown(
    "Toh doston, chinta mat karo, **life ka UPI PIN strong rakho, relationships ka OTP safe rakho, aur success ka QR Code scan karne ki koshish karte raho!** 😆🔥\n\n"
)

# UPI QR Code Image
upi_qr_code = "qrcode.jpg"
st.image(upi_qr_code, caption="Scan to Donate via UPI", width=150)

# Payment Link
st.write("[Donate via UPI (Click to Pay)](upi://pay?pa=ankle643@sbi&pn=Ankit%20Kumar&mc=0000&tid=9876543210&tr=BCR2DN4T&tn=Thanks%20for%20supporting!)")

st.write("Developed by Ankit Shrivastava")
