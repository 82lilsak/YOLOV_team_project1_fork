import cv2
import numpy as np
import threading
import time
import pyautogui
import handtrackingmodule as ht
import speech_recognition as sr
import math
from playsound import playsound
from queue import Queue
from pydub import AudioSegment
from pydub.playback import play
import webbrowser

#r = sr.Recognizer()

# 음성 명령에 대한 음악 파일 경로 설정
music_path = "C:/Users/user/AppData/Local/Temp/Love Hate.mp3"

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
minValue = volRange[0]
maxValue = volRange[1]

# # OpenCV GPU 모듈을 로드
cv2.ocl.setUseOpenCL(True)
cv2.setUseOptimized(True)

# 웹캠 화면 크기 설정 (1920x1080)
cap = cv2.VideoCapture(0)
cap.set(3, 700)
cap.set(4, 700)

# 손 추적 모듈 초기화
hand_tracking = ht.Hands()
ptime = 0
volBar = 400
volPer = 0

# Queue를 생성하여 스레드 간 통신
speech_queue = Queue()
music_queue = Queue()

play_music=False

def speech_recognition_thread(queue):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio)
                queue.put(command.lower())
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass

# 멀티스레딩 시작
speech_thread = threading.Thread(target=speech_recognition_thread, args=(speech_queue,))
speech_thread.daemon = True
speech_thread.start()

# 음악 재생을 관리하는 플래그
#play_music = False

def play_music_thread(queue):
    global play_music
    while True:
        if not queue.empty():
            play_music = True

        if play_music:
            sound = AudioSegment.from_mp3(music_path)
            play(sound)
            play_music = False



# 멀티스레딩 시작
music_play_thread = threading.Thread(target=play_music_thread, args=(music_queue,))
music_play_thread.daemon = True
music_play_thread.start()

# 이전 커서 위치 초기화
prevX, prevY = 0, 0

while True:
    # 비디오 프레임 읽기
    ret, frame = cap.read()

    if ret:
        # 손을 찾고 손의 특징점을 감지
        frame = hand_tracking.findHands(frame, draw=True)
        lmList = hand_tracking.findPosition(frame, draw=False)

        # 음성 명령을 확인
        while not speech_queue.empty():
            command = speech_queue.get()
            if "play" in command:
                music_queue.put(True)

            elif "search" in command:
                # 검색할 때 사용할 검색 엔진을 설정 (여기서는 구글)
                search_engine = "https://www.google.com/search?q="

                # 검색어 추출 (예: "search Python programming")
                search_query = "인텔 엣지ai".join(command.split()[1:])

                # 웹 브라우저로 검색 열기
                webbrowser.open(search_engine + search_query)
            # elif "stop" in command:
            #     pyautogui.press('space')  # Assuming space pauses the media player

        if len(lmList) != 0:
            # 엄지손가락과 중지손가락의 위치 가져오기
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            # 손가락 끝 부분에 원 그리기
            cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)

            # 엄지와 중지 사이에 선 그리기
            cv2.line(frame, (x1, y1), (x2, y2), (255, 100, 255), 3)

            # 선의 중간 지점 계산
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # 중간 지점에 원 그리기
            cv2.circle(frame, (cx, cy), 10, (255, 100, 255), cv2.FILLED)

            # 두 손가락 사이의 거리 계산
            length = math.hypot(x2 - x1, y2 - y1)

            # 거리를 볼륨 범위로 변환
            vol = np.interp(length, [18, 260], [minValue, maxValue])

            # 거리에 따라 볼륨 바와 백분율 조정
            volBar = np.interp(length, [18, 260], [400, 150])
            volPer = np.interp(length, [18, 260], [0, 100])

            # 볼륨 설정
            volume.SetMasterVolumeLevel(vol, None)

            # # 손의 위치에 따라 마우스 커서 이동 (보간 사용)
            # screenWidth, screenHeight = pyautogui.size()
            # moveX = np.interp(cx, [0, screenWidth], [0, screenWidth])
            # moveY = np.interp(cy, [0, screenHeight], [0, screenHeight])
            #
            # # 현재 커서 위치와 새로운 위치 사이를 보간하여 부드러운 이동 효과 생성
            # moveX = prevX + 0.2 * (moveX - prevX)
            # moveY = prevY + 0.2 * (moveY - prevY)
            #
            # # 커서 위치 업데이트
            # pyautogui.moveTo(moveX, moveY)
            #
            # # 현재 커서 위치를 이전 위치로 저장
            # prevX, prevY = moveX, moveY

        # 프레임 속도 계산
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        # 화면에 FPS 및 볼륨 바 출력
        cv2.putText(frame, f'FPS: {int(fps)}', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 100, 100), 2)
        cv2.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(frame, (50, int(volBar)), (85, 400), (255, 100, 100), cv2.FILLED)
        cv2.putText(frame, f'{int(volPer)}%', (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 100, 100), 4)

        # 화면 표시
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('1'):
            break

            # 음성 인식을 통해 음악을 재생 또는 멈춤

        # r = sr.Recognizer()
        # with sr.Microphone() as source:
        #     audio = r.listen(source)
        #     try:
        #         command = r.recognize_google(audio)
        #         if "play" in command.lower():
        #             playsound(music_path)
        #         elif "stop" in command.lower():
        #             playsound(None)  # Stop playing music
        #     except sr.UnknownValueError:
        #         pass
        #     except sr.RequestError:
        #         pass
    else:
        break