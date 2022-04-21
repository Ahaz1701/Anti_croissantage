### Made by Ahaz1701
### Fini les croissantages !!! :D

import os
import sys
import face_recognition
import cv2
import numpy as np
import timeit
import platform
import ctypes

ERROR = "[ERROR] No image detected. Need to access to your camera!"
INSTRUCTION = "[INSTRUCTION] Press 'y' to capture your face."

def initialization():
    if not os.path.isfile("me.png"):
        video_capture = cv2.VideoCapture(0)
        if video_capture is None or not video_capture.isOpened():
            sys.exit(ERROR)
        print(INSTRUCTION)

        while True:
            ret, frame = video_capture.read()
            if ret:
                cv2.imshow(INSTRUCTION, frame)
                if cv2.waitKey(1) & 0xFF == ord('y'):
                    cv2.imwrite("me.png", frame)
                    break
            else:
                sys.exit(ERROR)
        video_capture.release()
        cv2.destroyAllWindows()


def find_my_face():
    me = face_recognition.load_image_file("me.png")
    my_face_encoding = face_recognition.face_encodings(me)[0]

    known_face_encodings = [my_face_encoding]
    known_face_names = ["Ahaz"]

    video_capture = cv2.VideoCapture(0)
    if video_capture is None or not video_capture.isOpened():
        sys.exit(ERROR)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    start = timeit.default_timer()

    while True:
        ret, frame = video_capture.read()
        if ret:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unkown"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        start = timeit.default_timer()

                    face_names.append(name)

            process_this_frame = not process_this_frame

            end = timeit.default_timer()

            if end - start > 15:
                if platform.system() == "Linux":
                    os.popen("dbus-send --type=method_call --dest=org.gnome.ScreenSaver /org/gnome/ScreenSaver org.gnome.ScreenSaver.Lock")
                elif platform.system() == "Windows":
                    ctypes.windll.user32.LockWorkStation()

        else:
            sys.exit(ERROR)

if __name__ == "__main__":
    initialization()
    find_my_face()
    