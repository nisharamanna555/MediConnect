from pytube import YouTube

def download_video(youtube_url):
  # download YouTube video
  yt = YouTube(youtube_url)
  stream = yt.streams.get_highest_resolution()
  stream.download()
  print(f"Downloaded video for URL: {youtube_url}")

def download_video(youtube_url):
  # download YouTube video
  yt = YouTube(youtube_url)
  stream = yt.streams.get_highest_resolution()
  stream.download()
  print(f"Downloaded video for URL: {youtube_url}")

download_video('https://www.youtube.com/watch?v=Rdb3p9RZoR4')