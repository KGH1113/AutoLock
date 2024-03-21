import cv2
import os
import time
import ctypes

import sys
import subprocess
import time

from dotenv import load_dotenv

load_dotenv(verbose=True)


def lock_windows_screen():
    subprocess.call(["rundll32.exe", "user32.dll,LockWorkStation"])


def lock_mac_screen():
    applescript = """
    tell application "System Events" to keystroke "q" using {control down, command down}
    """
    subprocess.call(["osascript", "-e", applescript])


def lock_screen():
    if sys.platform.startswith("win"):
        lock_windows_screen()
    elif sys.platform.startswith("darwin"):
        lock_mac_screen()
    else:
        print("Unsupported operating system")


def main(name, id):
    def recognize(name_id, face_classifier, model, min_accuracy, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 얼굴 검출 ---④
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        msg = None
        accuracy = None
        for x, y, w, h in faces:
            face = frame[y : y + h, x : x + w]
            face = cv2.resize(face, (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            _, confidence = model.predict(face)
            accuracy = int(100 * (1 - confidence / 400))
            if accuracy >= min_accuracy:
                msg = name_id
            else:
                msg = "Unknown"

        return (faces, msg)

    crrnt_directory = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.join(crrnt_directory, "faces", "")
    min_accuracy = 87

    name_id = name + "_" + id

    face_classifier = cv2.CascadeClassifier(
        os.path.join(crrnt_directory, "haarcascade_frontalface_default.xml")
    )
    model = cv2.face.LBPHFaceRecognizer_create()
    print(base_dir + name_id + "all_face.xml")
    model.read(base_dir + name_id + "all_face.xml")

    cap = cv2.VideoCapture(int(os.environ["CAM_NUMBER"]))
    isOnCap = False
    start_time = 0
    end_time = 0
    while cap.isOpened():
        succes, image = cap.read()
        if not succes:
            print("Ignoring empty camera frame!")
            continue

        faces, msg = recognize(
            name_id, face_classifier, model, min_accuracy, frame=image
        )

        if msg == name_id:
            isOnCap = True
            for x, y, w, h in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 2)
                txt, base = cv2.getTextSize(msg, cv2.FONT_HERSHEY_PLAIN, 1, 3)
                cv2.rectangle(
                    image,
                    (x, y - base - txt[1]),
                    (x + txt[0], y + txt[1]),
                    (0, 255, 255),
                    -1,
                )
                cv2.putText(
                    image,
                    msg,
                    (x, y),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (200, 200, 200),
                    2,
                    cv2.LINE_AA,
                )

        else:
            if isOnCap:
                isOnCap = False
                start_time = time.time()
            elif not isOnCap:
                end_time = time.time()
                gap = end_time - start_time
                print(gap)
                if gap >= 3:
                    lock_screen()

        cv2.imshow("Autolock", image)
        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    main(name="KGH1113", id="1")
