from pytube import YouTube

def download(url, path):
  video_object = YouTube(url)
  streams = video_object.streams.filter(only_video=True, progressive=False, file_extension='mp4')
  video = streams._filter([lambda x: int(x.resolution[:-1]) <= 720 ])

  if video:
    video.first().download(path)
    return True
  else:
    return False