# import pytube
# from pydub import AudioSegment
# from pydub.playback import play
#
# youtube_url = "https://youtu.be/5LLu-WKm74I?si=ia3k8hiOlF3XsF3b"
#
# # PyTube를 사용하여 유튜브 동영상 다운로드
# # video = pytube.YouTube(youtube_url)
# # stream = video.streams.get_audio_only()
# # stream.download(output_path="C:/Users/wjgk0/Downloads/Project_Gesture_Volume_Control_Recording/Project_Gesture_Volume_Control_Recording/downloaded_audio")
#
# mp4_audio=AudioSegment.from_file("C:/Users/wjgk0/Downloads/Project_Gesture_Volume_Control_Recording/Project_Gesture_Volume_Control_Recording/downloaded_audio/Ai Uta.mp4",format="mp4")
#
# mp4_audio.export("C:/Users/wjgk0/Downloads/Project_Gesture_Volume_Control_Recording/Project_Gesture_Volume_Control_Recording/downloaded_audio/uta.mp3")
#
# # mp4_audio = AudioSegment.from_file("C:/Users/wjgk0/Downloads/Project_Gesture_Volume_Control_Recording/Project_Gesture_Volume_Control_Recording/downloaded_audio/audio", format="mp4")
# # mp4_audio.export("downloaded_audio/audio.mp3", format="mp3")
# #
# # # MP3 파일 재생
# # audio = AudioSegment.from_mp3("downloaded_audio/audio.mp3")
# #
# # # 음악 재생
# # play(audio)

import youtube_dl
from pydub import AudioSegment
from pydub.playback import play
import ffmpeg

youtube_url = "https://youtu.be/XFCVW1gjuBQ?si=ZT7bpj0IxXUc7MGE"

# YouTubeDL 객체 생성
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'postprocessor_args': ['-ar', '44100'],
    'prefer_ffmpeg': True,
    'keepvideo': False,
    'outtmpl': 'downloaded_audio/%(title)s.%(ext)s',
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(youtube_url, download=True)

# #MP3 파일 재생
# audio = AudioSegment.from_mp3("")
# play(audio)

# input_file="C:/Users/wjgk0/Downloads/Project_Gesture_Volume_Control_Recording/Project_Gesture_Volume_Control_Recording/downloaded_audio/Ai Uta.webm"
#
# output_file = "C:/Users/wjgk0/Downloads/Project_Gesture_Volume_Control_Recording/Project_Gesture_Volume_Control_Recording/downloaded_audio"
#
# # FFmpeg를 사용하여 WebM 파일을 MP3 파일로 변환
# input_stream = ffmpeg.input(input_file)
# output_stream = ffmpeg.output(input_stream, output_file, acodec="mp3", ar=44100)
# ffmpeg.run(output_stream, overwrite_output=True)
