# 1. Read the Live Webcam Feed
# 2. Resize the frame to (1280, 720) and flip it
# 3. Created a utils.py file and written the code for the handtracking module
# 4. Call the hand tracking module
# 5. Overlay both bat images
# 6. Draw the Ball
# 7. When the Ball hit the Vertical and Horizontal Walls it should Bounce
# 8. Check if the Bat is hitting the Ball or not so we can count the score
# 9. Fix the bounce by pushing the ball in the x-direction
# 10. Count the Score
# 11. Add a game over flag
import cv2
import utils as ht
import numpy as np
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
# handTracking = ht.HandDetector()
# imageFrontDesign = cv2.imread("Resources/FrontDesign.png")
# imageGameOver = cv2.imread("Resources/gameover.png")
# imageBat1 = cv2.imread("Resources/imgbat1.png", cv2.IMREAD_UNCHANGED)
# imageBat2 = cv2.imread("Resources/imgbat2.png", cv2.IMREAD_UNCHANGED)
# imageBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
#
# ball_position=[191, 82]
# speedX = 15
# speedY = 15
# score = [0,0]
# gameOver=False
# while True:
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.resize(frame, (1280, 720))
#         frame = cv2.flip(frame, 1)
#         framecopy = frame.copy()
#         #frame = handTracking.findHands(frame, draw=True)
#         frame, hands = handTracking.findPosition(frame, draw=True)
#         frame = cv2.addWeighted(frame, 0.3,imageFrontDesign, 0.7, 0)
#         if hands:
#             for hand in hands:
#                 x,y,w,h = hand["bbox"]
#                 h1, w1, _ = imageBat1.shape
#                 y1 = y - h1//2
#                 y1 = np.clip(y1, 45, 510)
#                 if hand["type"] == "Left":
#                     frame = ht.overlayPNG(frame, imageBat1, (73, y1))
#                     if 73 < ball_position[0] < 73 + w1 and y1 < ball_position[1] < y1 + h1:
#                         speedX = - speedX
#                         ball_position[0] += 30
#                         score[0]+=1
#                 if hand["type"] == "Right":
#                     frame = ht.overlayPNG(frame, imageBat2, (1192, y1))
#                     if 1192 - 60 < ball_position[0] < 1192 - 30 and y1 < ball_position[1] < y1 + h1:
#                         speedX = - speedX
#                         ball_position[0] -= 30
#                         score[1] += 1
#         # Move the Ball
#         ball_position[0] += speedX
#         ball_position[1] += speedY
#         #Draw the Ball
#         frame = ht.overlayPNG(frame, imageBall, (ball_position[0], ball_position[1]))
#
#         # When the Ball hit the Vertical and Horizontal Walls it should Bounce
#         if ball_position[1] >= 480 or ball_position[1] <= 22:
#             speedY = - speedY
#
#         # Display the Score
#         cv2.putText(frame, str(score[0]), (288, 651), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255, 255),5)
#         cv2.putText(frame, str(score[1]), (988, 651), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255, 255),5)
#
#         if ball_position[0] < 16 or ball_position[0] > 1276:
#             gameOver=True
#         if gameOver:
#             frame = imageGameOver
#             cv2.putText(frame, str(score[1] + score[0]).zfill(2), (604, 372), cv2.FONT_HERSHEY_COMPLEX, 2.5, (255, 100, 100), 5)
#         frame[556:700, 21:190] = cv2.resize(framecopy, (169, 144))
#         cv2.imshow("Live Webcam Feed", frame)
#         if cv2.waitKey(1) & 0xFF == ord('r'):
#             ball_position = [191, 82]
#             speedX = 15
#             speedY = 15
#             score = [0, 0]
#             gameOver = False
#             imageGameOver = cv2.imread("Resources/gameover.png")
#
#     else:
#         break

def run_game():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    handTracking = ht.HandDetector()
    imageFrontDesign = cv2.imread("Resources/FrontDesign.png")
    imageGameOver = cv2.imread("Resources/gameover.png")
    imageBat1 = cv2.imread("Resources/imgbat1.png", cv2.IMREAD_UNCHANGED)
    imageBat2 = cv2.imread("Resources/imgbat2.png", cv2.IMREAD_UNCHANGED)
    imageBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)

    ball_position = [191, 82]
    speedX = 15
    speedY = 15
    score = [0, 0]
    gameOver = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (1280, 720))
        frame = cv2.flip(frame, 1)
        framecopy = frame.copy()

        frame, hands = handTracking.findPosition(frame, draw=True)
        frame = cv2.addWeighted(frame, 0.3, imageFrontDesign, 0.7, 0)

        if hands:
            for hand in hands:
                x, y, w, h = hand["bbox"]
                h1, w1, _ = imageBat1.shape
                y1 = y - h1//2
                y1 = np.clip(y1, 45, 510)
                if hand["type"] == "Left":
                    frame = ht.overlayPNG(frame, imageBat1, (73, y1))
                    if 73 < ball_position[0] < 73 + w1 and y1 < ball_position[1] < y1 + h1:
                        speedX = -speedX
                        ball_position[0] += 30
                        score[0] += 1
                if hand["type"] == "Right":
                    frame = ht.overlayPNG(frame, imageBat2, (1192, y1))
                    if 1192 - 60 < ball_position[0] < 1192 - 30 and y1 < ball_position[1] < y1 + h1:
                        speedX = -speedX
                        ball_position[0] -= 30
                        score[1] += 1

        ball_position[0] += speedX
        ball_position[1] += speedY

        frame = ht.overlayPNG(frame, imageBall, (ball_position[0], ball_position[1]))

        if ball_position[1] >= 480 or ball_position[1] <= 22:
            speedY = -speedY

        cv2.putText(frame, str(score[0]), (288, 651), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(frame, str(score[1]), (988, 651), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

        if ball_position[0] < 16 or ball_position[0] > 1276:
            gameOver = True
        if gameOver:
            frame = imageGameOver
            cv2.putText(frame, str(score[1] + score[0]).zfill(2), (604, 372), cv2.FONT_HERSHEY_COMPLEX, 2.5,
                        (255, 100, 100), 5)

        frame[556:700, 21:190] = cv2.resize(framecopy, (169, 144))
        cv2.imshow("Live Webcam Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('r'):
            ball_position = [191, 82]
            speedX = 15
            speedY = 15
            score = [0, 0]
            gameOver = False
            imageGameOver = cv2.imread("Resources/gameover.png")

        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()