# import cv2
# import os
# import handtrackingmodule as ht
#
# # Initialize Hand Tracking module
# hand_tracking = ht.Hands()
#
# # Variables to track hand position
# prev_x, prev_y = 0, 0
#
# # Main loop
# cap = cv2.VideoCapture(0)
#
# while True:
#     ret, frame = cap.read()
#
#     if ret:
#         # Find hands and get landmark positions
#         frame = hand_tracking.findHands(frame, draw=True)
#         lmList = hand_tracking.findPosition(frame, draw=False)
#
#         if lmList:
#             # Get the coordinates of the tip of the index finger (landmark 8)
#             x, y = lmList[8][1], lmList[8][2]
#
#             # Check if the hand is in a specific region of the screen
#             if 100 < x < 200 and 300 < y < 400:
#                 # Check if the hand is moving from left to right
#                 if x > prev_x:
#                     # Open the file explorer (Windows specific)
#                     os.system("explorer")
#
#             prev_x, prev_y = x, y
#
#         # Display the frame
#         cv2.imshow("Hand Tracking", frame)
#
#         # Check for key press (press 'q' to exit)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import handtrackingmodule as ht
# import subprocess
#
# # Initialize Hand Tracking module
# hand_tracking = ht.Hands()
#
# # Variables to track hand position
# prev_x, prev_y = 0, 0
# frames_with_hand = 0  # Number of frames with hand in a specific region
#
# # Main loop
# cap = cv2.VideoCapture(0)
#
# while True:
#     ret, frame = cap.read()
#
#     if ret:
#         # Find hands and get landmark positions
#         frame = hand_tracking.findHands(frame, draw=True)
#         lmList = hand_tracking.findPosition(frame, draw=False)
#
#         if lmList:
#             # Get the coordinates of the tip of the index finger (landmark 8)
#             x, y = lmList[8][1], lmList[8][2]
#
#             # Check if the hand is in a specific region of the screen
#             if 100 < x < 200 and 300 < y < 400:
#                 frames_with_hand += 1
#                 if frames_with_hand >= 10:
#                     # Open the file explorer (Windows specific)
#                     subprocess.Popen('explorer')
#                     frames_with_hand = 0
#             else:
#                 frames_with_hand = 0
#
#         # Display the frame
#         cv2.imshow("Hand Tracking", frame)
#
#         # Check for key press (press 'q' to exit)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import handtrackingmodule as ht
# import os
# import subprocess
#
# # Initialize Hand Tracking module
# hand_tracking = ht.Hands()
#
# # Set the region where hand gesture triggers the action
# region_x = (150, 350)  # X-coordinates of the region
# region_y = (300, 500)  # Y-coordinates of the region
#
# # Main loop
# cap = cv2.VideoCapture(0)
#
# while True:
#     ret, frame = cap.read()
#
#     if ret:
#         # Find hands and get landmark positions
#         frame = hand_tracking.findHands(frame, draw=True)
#         lmList = hand_tracking.findPosition(frame, draw=False)
#
#         if lmList:
#             # Get the coordinates of the tip of the index finger (landmark 8)
#             x, y = lmList[8][1], lmList[8][2]
#
#             # Check if the hand is in the region where action is triggered
#             if region_x[0] < x < region_x[1] and region_y[0] < y < region_y[1]:
#                 subprocess.Popen('explorer')
#                 # Open the file explorer (Windows specific)
#                 #os.system('explorer')
#                 #break  # Exit the loop after opening the file explorer
#
#         # Display the frame
#         cv2.imshow("Hand Tracking", frame)
#
#         # Check for key press (press 'q' to exit)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# cap.release()
# cv2.destroyAllWindows()


import cv2
import handtrackingmodule as ht
import os

# Initialize Hand Tracking module
hand_tracking = ht.Hands()

# Set the region where hand gesture triggers the action
region_x = (150, 350)  # X-coordinates of the region
region_y = (300, 500)  # Y-coordinates of the region

# Flag to keep track of whether file explorer is opened
explorer_opened = False

# Main loop
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if ret:
        # Find hands and get landmark positions
        frame = hand_tracking.findHands(frame, draw=True)
        lmList = hand_tracking.findPosition(frame, draw=False)

        if lmList:
            # Get the coordinates of the tip of the index finger (landmark 8)
            x, y = lmList[8][1], lmList[8][2]

            # Check if the hand is in the region where action is triggered
            if region_x[0] < x < region_x[1] and region_y[0] < y < region_y[1]:
                if not explorer_opened:
                    # Open the file explorer (Windows specific)
                    os.system('explorer')
                    explorer_opened = True  # Set the flag to True

        # Display the frame
        cv2.imshow("Hand Tracking", frame)

        # Check for key press (press 'q' to exit)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()



