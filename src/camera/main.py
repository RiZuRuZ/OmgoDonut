import cv2
import numpy as np
import serial

ser = serial.Serial("Com3", 115200)
cap = cv2.VideoCapture(0)
ser_write = False

if not cap.isOpened():
    exit()
"""
Orange 0-22
Yellow 22-38
Green 38-75
Blue 75-130
Violet 130-160
Red 160-179
"""

H_HSV_lower_setup = {
    "Orange": [0, 100, 100],
    "Yellow": [23, 100, 100],
    "Green": [39, 100, 100],
    "Blue": [76, 100, 100],
    "Violet": [131, 100, 100],
    "Red": [161, 100, 100],
}

H_HSV_upper_setup = {
    "Orange": [22, 255, 255],
    "Yellow": [38, 255, 255],
    "Green": [75, 255, 255],
    "Blue": [130, 255, 255],
    "Violet": [160, 255, 255],
    "Red": [179, 255, 255],
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_Red = np.array(H_HSV_lower_setup["Red"])
    upper_Red = np.array(H_HSV_upper_setup["Red"])

    lower_Green = np.array(H_HSV_lower_setup["Green"])
    upper_Green = np.array(H_HSV_upper_setup["Green"])

    lower_Violet = np.array(H_HSV_lower_setup["Violet"])
    upper_Violet = np.array(H_HSV_upper_setup["Violet"])

    detect_Red = cv2.inRange(hsv, lower_Red, upper_Red)
    detect_Green = cv2.inRange(hsv, lower_Green, upper_Green)
    detect_Violet = cv2.inRange(hsv, lower_Violet, upper_Violet)

    contours1, hierarchy1 = cv2.findContours(
        detect_Red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )  # Finding contours in mask image
    contours2, hierarchy2 = cv2.findContours(
        detect_Green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours3, hierarchy3 = cv2.findContours(
        detect_Violet, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    counter = 0
    memory = ""

    # Finding position of all contours
    if len(contours1) != 0:
        for contour in contours1:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(
                    frame, (x, y), (x + w, y + h), (0, 0, 255), 3
                )  # drawing rectangle
                counter += 1
                memory = "Red"

    if len(contours2) != 0:
        for contour in contours2:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(
                    frame, (x, y), (x + w, y + h), (0, 0, 255), 3
                )  # drawing rectangle
                counter += 1
                memory = "Green"

    if len(contours3) != 0:
        for contour in contours3:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(
                    frame, (x, y), (x + w, y + h), (0, 0, 255), 3
                )  # drawing rectangle
                counter += 1
                memory = "Violet"

    if counter == 1:
        if not ser_write:
            if memory == "Red":
                print("Red")
                print(counter)
                ser.write(b"Red\r\n")
            elif memory == "Green":
                print("Green")
                print(counter)
                ser.write(b"Green\r\n")
            elif memory == "Violet":
                print("Violet")
                print(counter)
                ser.write(b"Violet\r\n")
            else:
                print("error")
            ser_write = True
    else:
        if ser_write:
            print(counter)
            # ser.write(b"0\r\n")
            ser_write = False

    cv2.putText(
        frame,
        str(counter),
        (10, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        3,
        [0, 0, 255],
        3,
        cv2.LINE_AA,
    )
    cv2.imshow("frame", frame)
    cv2.imshow("DetectedR", detect_Red)
    cv2.imshow("DetectedG", detect_Green)
    cv2.imshow("DetectedV", detect_Violet)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
