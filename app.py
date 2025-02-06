from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Directory to store downloaded files
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "YouTube Downloader API is running!"

@app.route("/download", methods=["POST"])
def download_video():
    data = request.json
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Set download options
        ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    'format': 'bestvideo+bestaudio/best',
    'cookiefile': 'cookies.txt'  # Add this line to use cookies

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({"message": "Download complete!", "file": filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
