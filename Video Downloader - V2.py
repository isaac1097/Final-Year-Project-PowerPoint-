import os
import shutil
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def sanitize_filename(title):
    return title.replace(':', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')

def create_video_folder(path, title):
    sanitized_title = sanitize_filename(title)
    video_folder = os.path.join(path, sanitized_title)
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    return video_folder

def copy_subtitle_to_fixed_folder(subtitle_file_path, fixed_folder):
    try:
        if not os.path.exists(fixed_folder):
            os.makedirs(fixed_folder)
        shutil.copy(subtitle_file_path, fixed_folder)
    except Exception as e:
        print(f"Error copying subtitle file to the fixed folder. Error: {e}")

def download_video_and_subtitles(url, path, fixed_folder, max_retries=30):
    retries = 0
    while retries < max_retries:
        try:
            yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)

            video_folder = create_video_folder(path, yt.title)

            stream = yt.streams.get_highest_resolution()

            print(f"Downloading video: {yt.title}")
            stream.download(video_folder)
            print(f"Video {yt.title} downloaded successfully.")

            try:
                transcript = YouTubeTranscriptApi.get_transcript(yt.video_id, languages=["en"])
                subtitle_text = "\n".join([entry["text"] for entry in transcript])

                sanitized_title = sanitize_filename(yt.title)
                subtitle_file_path = os.path.join(video_folder, f"{sanitized_title}_subtitles.txt")
                with open(subtitle_file_path, "w", encoding="utf-8") as f:
                    f.write(subtitle_text)
                print(f"Subtitles for {yt.title} downloaded successfully to: {subtitle_file_path}")

                copy_subtitle_to_fixed_folder(subtitle_file_path, fixed_folder)

            except Exception as e:
                print(f"No English subtitles available for {yt.title}. Error: {e}")

            break

        except Exception as e:
            print(f"Error downloading video or subtitles: {url}")
            print(e)
            retries += 1
            print(f"Retry {retries} of {max_retries}")
            if retries >= max_retries:
                print(f"Failed to download video or subtitles after {max_retries} retries.")

if __name__ == "__main__":
    # Path to the text file containing video URLs, one URL per line
    url_file_path = r"C:\Users\Isaac\Desktop\NTU\Y3S2\FYP\Misc Stuff\Test\video_urls.txt"

    # Read video URLs from the file
    with open(url_file_path, "r") as url_file:
        video_urls = [line.strip() for line in url_file]

    # Path to save the downloaded videos and subtitles
    download_path = r"C:\Users\Isaac\Desktop\NTU\Y3S2\FYP\Misc Stuff\Test"

    # Fixed folder to store all the subtitle files
    fixed_folder = r"C:\Users\Isaac\Desktop\NTU\Y3S2\FYP\Misc Stuff\Test"
    
    # Download all videos and subtitles in the list
    for url in video_urls:
        download_video_and_subtitles(url, download_path, fixed_folder)

