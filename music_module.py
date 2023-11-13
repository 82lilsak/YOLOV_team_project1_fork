from pydub import AudioSegment
from pydub.playback import play
from queue import Queue

music_path = "D:/AI_exam/YOLOV_team_project/downloaded_audio/萩原 雪歩 - Agape (cover).mp3"

music_path2="D:/AI_exam/YOLOV_team_project/downloaded_audio/『Lyrics AMV』Boku no Kokoro no Yabai Yatsu【Shayou - Yorushika】Opening Full.mp3"

play_music=False
def play_music_thread(queue):

    global play_music

    while True:
        if not queue.empty():
            play_music = True

        if play_music:
            sound = AudioSegment.from_mp3(music_path)
            play(sound)
            play_music = False


def play_music_thread2(queue):

    global play_music

    play_music = False

    while True:
        if not queue.empty():
            play_music = True

        if play_music:
            sound = AudioSegment.from_mp3(music_path2)
            play(sound)
            play_music = False