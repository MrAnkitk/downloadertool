import streamlit as st
import yt_dlp
import os

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

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
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    
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
            file_path = download_media(url, quality)
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

# If download completed, show popup 
if "download_completed" in st.session_state and st.session_state.download_completed:
    with st.expander("🎉 Download Successful! Click to Support 🎉", expanded=True):
        st.markdown("## 🤑 *Yaar! Ek Cup Chai Toh Banta Hai!* ☕")
        
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
