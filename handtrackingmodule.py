import cv2
import mediapipe as mp

class Hands():
    def __init__(self, mode=False, max_Hands=2, mcomplexity = 1, detectionCon=0.8, trackCon=0.5):
        self.mode = mode
        self.max_Hands = max_Hands
        self.mcomplexity = mcomplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_Hands,self.mcomplexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                #print(handLMS)
                self.mpDraw.draw_landmarks(img, handLMS, self.mpHands.HAND_CONNECTIONS)

        return img
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            lmList=[]
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 100, 100), cv2.FILLED)
        return lmList