import cv2
import numpy as np
import time
import autopy
from cvzone.HandTrackingModule import HandDetector
from pythonosc.udp_client import SimpleUDPClient
import socket

# OSC Setup
UDP_IP = "127.0.0.1"
UDP_PORT = 7000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ------------------------ Camera Setup ------------------------
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# ------------------------ Hand Detector ------------------------
detector = HandDetector(detectionCon=0.8, maxHands=2)

# ------------------------ Virtual Mouse Setup ------------------------
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
click_delay = 0.5
last_click_time = 0

# Screen size
wScr, hScr = autopy.screen.size()

# Previous locations
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# On Gesture Changed
last_gesture = -1  # Invalid initial state

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # Flip for natural interaction

    # ------------------------ Hand Detection ------------------------
    hands, frame = detector.findHands(frame, draw=False, flipType=False)

    #default gesture value
    gesture_value = 0

    for hand in hands:
        fingers = detector.fingersUp(hand)
        handType = hand["type"]
        lmList = hand["lmList"]

        # ------------------------ Left Hand Gesture Detection ------------------------
        if handType == "Left":
            #print("Left fingers:", fingers)

            if fingers == [1, 1, 0, 0, 0]:
                gesture_value = 0
                print("one")
            elif fingers == [1, 1, 1, 0, 0]:
                gesture_value = 1
                print("two")
            elif fingers == [1, 1, 1, 1, 0]:
                gesture_value = 2
                print("three")
            else:
                gesture_value = 0
                print("one still")

        # ------------------------ Right Hand Virtual Mouse ------------------------
        elif handType == "Right":
            if fingers == [1, 1, 0, 0, 0]:
                x1, y1 = lmList[8][:2]  # Index finger tip
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                autopy.mouse.move(clocX, clocY)
                cv2.circle(frame, (x1, y1), 10, (200, 100, 0), cv2.FILLED)

                plocX, plocY = clocX, clocY

            elif fingers == [0, 1, 0, 0, 0]:
                current_time = time.time()
                if (current_time - last_click_time) > click_delay:
                    autopy.mouse.click()
                    last_click_time = current_time
                    x1, y1 = lmList[8][:2]
                    cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)

    #sock.sendto(str(gesture_value).encode(), (UDP_IP, UDP_PORT))
    # Send only on change
    if gesture_value != last_gesture:
        sock.sendto(str(gesture_value).encode(), (UDP_IP, UDP_PORT))
        last_gesture = gesture_value

    # ------------------------ FPS Display ------------------------
    curr_time = time.time()
    fps = 1 / (curr_time - last_click_time) if last_click_time != 0 else 0
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100, 0), 2)

    # ------------------------ Display Frame ------------------------
    cv2.imshow("Left Hand Gesture + Right Hand Virtual Mouse", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
