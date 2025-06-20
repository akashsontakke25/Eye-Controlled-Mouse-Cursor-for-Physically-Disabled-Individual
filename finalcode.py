import cv2
import face_recognition
import time
import numpy as np
from pynput.mouse import Button, Controller
import wx

mouse = Controller()
app = wx.App(False)
(sx, sy) = wx.GetDisplaySize()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)

known_image = cv2.imread('akash.jpg')
known_encoding = face_recognition.face_encodings(known_image)[0]

face_recognized = False  # Flag to track if face has been recognized
detection_count = 0  # Counter for number of detections

main_frame_x1 = 100
main_frame_y1 = 100
main_frame_x2 = 300
main_frame_y2 = 250

left_x1 = 30
left_y1 = 30
left_x2 = 80
left_y2 = 80

right_x1 = 500
right_y1 = 30
right_x2 = 550
right_y2 = 30

flag = 1
oldx = -1
oldy = -1
cnt = 0

def color_all():
    # rectange for left mouse
    cv2.rectangle(frame, (30, 30), (80, 80), (255, 0, 0), 3)
    cv2.rectangle(frame, (30, 30), (55, 55), (255, 0, 0), -1)

    # rectange for right mouse
    cv2.rectangle(frame, (130, 30), (180, 80), (255, 0, 0), 3)
    cv2.rectangle(frame, (155, 30), (180, 55), (255, 0, 0), -1)

    # rectange for double mouse
    cv2.rectangle(frame, (230, 30), (280, 80), (255, 0, 0), 3)
    cv2.rectangle(frame, (240, 40), (260, 60), (255, 0, 0), -1)
    cv2.rectangle(frame, (250, 50), (270, 70), (255, 0, 0), -1)

def color_left():
    # rectange for left mouse
    cv2.rectangle(frame, (30, 30), (80, 80), (0, 0, 255), 3)
    cv2.rectangle(frame, (30, 30), (55, 55), (0, 0, 255), -1)

def color_right():
    # rectange for right mouse
    cv2.rectangle(frame, (130, 30), (180, 80), (0, 0, 255), 3)
    cv2.rectangle(frame, (155, 30), (180, 55), (0, 0, 255), -1)

def color_double():
    # rectange for double mouse
    cv2.rectangle(frame, (230, 30), (280, 80), (0, 0, 255), 3)
    cv2.rectangle(frame, (240, 40), (260, 60), (0, 0, 255), -1)
    cv2.rectangle(frame, (250, 50), (270, 70), (0, 0, 255), -1)

while True:
    ret, frame = video_capture.read()

    if not face_recognized:
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if face_locations:
            detection_count += 1
            print(f"Face detected! Count: {detection_count}")
            
            if detection_count >= 5:
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                face_encoding = face_encodings[0]
                matches = face_recognition.compare_faces([known_encoding], face_encoding)

                if matches[0]:
                    print("Face recognized! Access granted.")
                    face_recognized = True  
                else:
                    print("Face not recognized. Access denied.")
                    break
                
                # Reset detection count and wait for 2 seconds
                detection_count = 0
                time.sleep(2)

    if face_recognized:
        color_all()
        if flag == 1:
            color_left()

        if flag == 2:
            color_right()

        if flag == 3:
            color_double()

        cv2.rectangle(frame, (main_frame_x1, main_frame_y1),
                      (main_frame_x2, main_frame_y2), (0, 0, 0), 2)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 10)

        mx = -1
        for (x, y, w, h) in faces:
            mx = max(mx, w*h)

        newx = -1
        newy = -1
        for (x, y, w, h) in faces:
            if (mx == w*h):
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                if x >= 30 and x <= 80 and y >= 30 and y <= 80:
                    flag = 1  # left click
                    color_all()
                    color_left()

                if x >= 130 and x <= 180 and y >= 30 and y <= 80:
                    flag = 2  # right click
                    color_all()
                    color_right()

                if x >= 230 and x <= 280 and y >= 30 and y <= 80:
                    flag = 3  # double click
                    color_all()
                    color_double()

                newx = x - main_frame_x1
                newy = y - main_frame_y1

                newx = (newx*sx)/(main_frame_x2-main_frame_x1)
                newy = (newy*sy)/(main_frame_y2-main_frame_y1)

                mouse.position = (newx, newy)

                if oldx == -1:
                    oldx = newx
                    oldy = newy
                else:
                    cnt = cnt + 1
                    if cnt < 10:
                        continue

                    if flag == 1:
                        mouse.click(Button.left, 1)
                    if flag == 2:
                        mouse.click(Button.right, 1)
                    if flag == 3:
                        mouse.click(Button.left, 2)

                    cnt = 0
                    oldx = newx
                    oldy = newy

                break

    cv2.imshow('Result', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
