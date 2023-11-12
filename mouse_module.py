import pyautogui
from queue import Queue

def move_mouse_thread(queue):
    global prevX, prevY
    # x1, y1 = lmList[4][1], lmList[4][2]
    #     # x2, y2 = lmList[8][1], lmList[8][2]
    #     # x3, y3 = lmList[12][1], lmList[12][2]
    #     # x4, y4 = lmList[16][1], lmList[16][2]
    #     # x5, y5 = lmList[20][1], lmList[20][2]
    while True:
        if not queue.empty():
            moveX, moveY = queue.get()

            moveX = prevX + 0.2 * (moveX - prevX)
            moveY = prevY + 0.2 * (moveY - prevY)

            pyautogui.moveTo(moveX, moveY)

            prevX, prevY = moveX, moveY


prevX, prevY = 0, 0
