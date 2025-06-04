import cv2
import numpy as np
import time
import autopy
import threading
from cvzone.HandTrackingModule import HandDetector
import socket

# Webcam setup
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
click_delay = 0.5  # Prevent accidental clicks
last_click_time = 0

# To print fps
pTime = 0

# Previous locations for smooth motion
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Capture video in a separate thread
cap = cv2.VideoCapture(1)

# Hand Detector
detector = HandDetector(detectionCon=0.65, maxHands=2)  # Lower confidence for speed

# Get screen resolution
wScr, hScr = autopy.screen.size()

# Zooming variables
startDist = None
scale = 0
cx, cy = 500, 500  # Center for zooming

# Load Image
img_overlay = cv2.imread("image.png")

# Setup UDP
UDP_IP = "127.0.0.1"  # TouchDesigner's IP (localhost)
UDP_PORT = 5005        # Port number (match with TouchDesigner)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create UDP socket

# --- Multi-threaded Frame Capture ---
frame = None
def capture_frame():
    global frame
    while True:
        success, frame = cap.read()

capture_thread = threading.Thread(target=capture_frame, daemon=True)
capture_thread.start()

while True:
    if frame is None:
        continue  # Wait until a frame is available

    img = frame.copy()
    hands, img = detector.findHands(img, draw=False)  # Don't draw landmarks unless needed



    # --- Check for Zoom Mode (Two Hands Detected) ---
    zooming = False
    if len(hands) == 2:
        hand1, hand2 = hands
        fingers1, fingers2 = detector.fingersUp(hand1), detector.fingersUp(hand2) #if these conditions are true

        if fingers1[:2] == [1, 1] and fingers2[:2] == [1, 1]:  # Only check first two fingers
            length, info, img = detector.findDistance(hand1["center"], hand2["center"], img)
            if startDist is None:
                startDist = length #find the distance between hands

            raw_scale = (length - startDist) / 250.0  # adjust 200.0 as needed for sensitivity
            scale = max(0.0, min(1.0, raw_scale))

            # Convert scale to string & send via UDP
            message = str(scale).encode()
            sock.sendto(message, (UDP_IP, UDP_PORT))

            cx, cy = info[4:]  # Midpoint of hands. Extract distance from findDistance lib
            zooming = True
            #print(scale)

            # --- Resize and Overlay Image ---
            try:
                h1, w1, _ = img_overlay.shape
                newH, newW = ((h1 + scale) // 2) * 2, ((w1 + scale) // 2) * 2
                img1 = cv2.resize(img_overlay, (newW, newH))
                # Get webcam frame size
                H, W, _ = img.shape
                # Calculate bounds to prevent overlaying outside the frame
                x1, y1 = max(0, cx - newW // 2), max(0, cy - newH // 2)
                x2, y2 = min(W, cx + newW // 2), min(H, cy + newH // 2)
                # Crop and overly img1 if it extends beyond the frame
                img_crop = img1[:y2 - y1, :x2 - x1]
                img[y1:y2, x1:x2] = img_crop

            except Exception as e:
                print("Overlay Error:", e)

        else:
            startDist = None

    # Virtual Mouse Mode (Only if NOT Zooming)
    if not zooming and len(hands) == 1:
        hand = hands[0] # Single detected hand
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand) #Check which fingers are up

        if fingers == [0, 1, 0, 0, 0]:  # Only index finger
            x1, y1 = lmList[8][:2]
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr)) # Convert Coordinates from webcam space to screen monitor space
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # Smoothen movement
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # We need to do a conversion due to coords system mismatch (OpenCV-autopy)
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 10, (200, 100, 0), cv2.FILLED)
            plocX, plocY = clocX, clocY
        # Clicking Mode: Click when index and middle fingers are up
        if fingers == [0, 1, 1, 0, 0]:
            length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
            current_time = time.time()
            if length < 30 and (current_time - last_click_time) > click_delay: #set threshold for clicking trigger
                autopy.mouse.click()
                last_click_time = current_time
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
    cv2.imshow("Virtual Mouse & Gesture Control", img)
    cv2.waitKey(1)
