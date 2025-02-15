import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from cvzone.SerialModule import SerialObject

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
mySerial = SerialObject("COM5", 9600, 1)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # With Draw
    # hands = detector.findHands(img, draw=False)  # No Draw

    if len(hands) == 1:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right

        # print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        fingers1 = detector.fingersUp(hand1)
        #length, info, img = detector.findDistance(lmList1[8], lmList1[12], img) # with draw
        #length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw
        zero_fing = [0,0,0,0,0]
        if handType1 == "Left":
            handType1 = fingers1 + zero_fing
        elif handType1 == "Right":
            handType1 = zero_fing + fingers1 
        mySerial.sendData(handType1)
        print(handType1)

    elif len(hands) == 2:
        hand1 = hands[0]
        hand2 = hands[1]
        lmList2 = hand2["lmList"]  # List of 21 Landmarks points
        bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
        centerPoint2 = hand2["center"]  # center of the hand cx,cy
        handType2 = hand2["type"]  # Hand Type Left or Right
        fingers1 = detector.fingersUp(hand1)
        fingers2 = detector.fingersUp(hand2)
        #print(fingers1, fingers2)
        #length, info, img = detector   .findDistance(lmList1[8], lmList2[8], img) # with draw
        #length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)  # with draw

        fingers_total = fingers1 + fingers2
        mySerial.sendData(fingers_total)
        print(fingers_total)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow("Image", img)
    cv2.waitKey(1)