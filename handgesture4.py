# import cv2
# import numpy as np
# import handtrackingmodule as ht
# import math
# import time
# import pyautogui
#
# # pycaw를 사용하여 오디오 제어를 위한 설정
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = interface.QueryInterface(IAudioEndpointVolume)
# volRange = volume.GetVolumeRange()
# minValue = volRange[0]
# maxValue = volRange[1]
#
# # 비디오 캡처 설정
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
#
# # 손 추적 모듈 초기화
# hand_tracking = ht.Hands()
# ptime = 0
# volBar = 400
# volPer = 0
#
# while True:
#     # 비디오 프레임 읽기
#     ret, frame = cap.read()
#
#     if ret:
#         # 손을 찾고 손의 특징점을 감지
#         frame = hand_tracking.findHands(frame, draw=True)
#         lmList = hand_tracking.findPosition(frame, draw=False)
#
#         if len(lmList) != 0:
#             # 엄지손가락과 중지손가락의 위치 가져오기
#             x1, y1 = lmList[4][1], lmList[4][2]
#             x2, y2 = lmList[8][1], lmList[8][2]
#
#             # 손가락 끝 부분에 원 그리기
#             cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
#             cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
#
#             # 엄지와 중지 사이에 선 그리기
#             cv2.line(frame, (x1, y1), (x2, y2), (255, 100, 255), 3)
#
#             # 선의 중간 지점 계산
#             cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
#
#             # 중간 지점에 원 그리기
#             cv2.circle(frame, (cx, cy), 10, (255, 100, 255), cv2.FILLED)
#
#             # 두 손가락 사이의 거리 계산
#             length = math.hypot(x2 - x1, y2 - y1)
#
#             # 거리를 볼륨 범위로 변환
#             vol = np.interp(length, [18, 260], [minValue, maxValue])
#
#             # 거리에 따라 볼륨 바와 백분율 조정
#             volBar = np.interp(length, [18, 260], [400, 150])
#             volPer = np.interp(length, [18, 260], [0, 100])
#
#             # 볼륨 설정
#             volume.SetMasterVolumeLevel(vol, None)
#
#             # 손의 위치에 따라 마우스 커서 이동
#             screenWidth, screenHeight = pyautogui.size()
#             moveX = np.interp(cx, [0, screenWidth], [0, screenWidth])
#             moveY = np.interp(cy, [0, screenHeight], [0, screenHeight])
#             pyautogui.moveTo(moveX, moveY)
#
#         # 프레임 속도 계산
#         ctime = time.time()
#         fps = 1 / (ctime - ptime)
#         ptime = ctime
#
#         # 화면에 FPS 및 볼륨 바 출력
#         cv2.putText(frame, f'FPS: {int(fps)}', (30, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 100, 100), 2)
#         cv2.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), 3)
#         cv2.rectangle(frame, (50, int(volBar)), (85, 400), (255, 100, 100), cv2.FILLED)
#         cv2.putText(frame, f'{int(volPer)}%', (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 100, 100), 4)
#
#         # 화면 표시
#         cv2.imshow("Video", frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('1'):
#             break
#     else:
#         break
#
# # 코드 실행 중 마우스 커서를 이동할 수 있으며, 볼륨을 조절할 수 있습니다. 웹캠을 사용하여 손 위치를 추적하고 해당 위치에 따라 마우스 커서를 제어할 수 있습니다.

import cv2
import numpy as np
import handtrackingmodule as ht
import math
import time
import pyautogui

# pycaw를 사용하여 오디오 제어를 위한 설정
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
cap.set(3, 1280)
cap.set(4, 720)

# 손 추적 모듈 초기화
hand_tracking = ht.Hands()
ptime = 0
volBar = 400
volPer = 0

# 이전 커서 위치 초기화
prevX, prevY = 0, 0

while True:
    # 비디오 프레임 읽기
    ret, frame = cap.read()

    if ret:
        # 손을 찾고 손의 특징점을 감지
        frame = hand_tracking.findHands(frame, draw=True)
        lmList = hand_tracking.findPosition(frame, draw=False)

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

            # 손의 위치에 따라 마우스 커서 이동 (보간 사용)
            screenWidth, screenHeight = pyautogui.size()
            moveX = np.interp(cx, [0, screenWidth], [0, screenWidth])
            moveY = np.interp(cy, [0, screenHeight], [0, screenHeight])

            # 현재 커서 위치와 새로운 위치 사이를 보간하여 부드러운 이동 효과 생성
            moveX = prevX + 0.2 * (moveX - prevX)
            moveY = prevY + 0.2 * (moveY - prevY)

            # 커서 위치 업데이트
            pyautogui.moveTo(moveX, moveY)

            # 현재 커서 위치를 이전 위치로 저장
            prevX, prevY = moveX, moveY

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
    else:
        break



