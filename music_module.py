from pydub import AudioSegment
from pydub.playback import play
from queue import Queue

music_path = "C:/Users/wjgk0/Downloads/Project_Gesture_Volume_Control_Recording/YOLOV_team_project1/downloaded_audio/萩原 雪歩 - Agape (cover).mp3"

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
