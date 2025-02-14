import yt_dlp

def download_video(url, quality="best", media_type="video"):
    format_map = {
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "360p": "bestvideo[height<=360]+bestaudio/best",
        "Audio Only": "bestaudio/best"
    }

    postprocessors = []
    
    if media_type == "audio":
        postprocessors.append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        })
    else:
        postprocessors.append({
            'key': 'FFmpegVideoRemuxer',
            'preferedformat': 'mp4'  # Corrected spelling mistake
        })

    options = {
        'format': format_map.get(quality, 'best'),
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': postprocessors
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print("✅ Download successful!")
    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage
video_url = input("Enter video URL: ")
media_choice = input("Download as (video/audio): ").strip().lower()
quality_choice = input("Choose quality (1080p, 720p, 480p, 360p, Audio Only): ").strip()

download_video(video_url, quality_choice, media_choice)
