import cv2
import numpy as np
import os, glob
from dotenv import load_dotenv

load_dotenv(verbose=True)


def main(name, id):
    ########### Colect ###########
    crrnt_directory = os.path.dirname(os.path.realpath(__file__))
    print(crrnt_directory)
    # 변수 설정 ---①
    base_dir = os.path.join(crrnt_directory, "faces")
    target_cnt = 500
    cnt = 0

    face_classifier = cv2.CascadeClassifier(
        os.path.join(crrnt_directory, "haarcascade_frontalface_default.xml")
    )

    dir = os.path.join(base_dir, name + "_" + id)
    if not os.path.exists(dir):
        os.mkdir(dir)

    cap = cv2.VideoCapture(int(os.environ["CAM_NUMBER"]))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            img = frame.copy()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 1:
                (x, y, w, h) = faces[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                face = gray[y : y + h, x : x + w]
                face = cv2.resize(face, (200, 200))
                file_name_path = os.path.join(dir, str(cnt) + ".jpg")
                cv2.imwrite(file_name_path, face)
                cv2.putText(
                    frame, str(cnt), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2
                )
                cnt += 1
            else:
                if len(faces) == 0:
                    msg = "no face."
                elif len(faces) > 1:
                    msg = "too many face."
                cv2.putText(
                    frame, msg, (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255)
                )
            cv2.imshow("face record", frame)
            if cv2.waitKey(1) == 27 or cnt == target_cnt:
                break
    cap.release()
    cv2.destroyAllWindows()
    print("Collecting Samples Completed.")
    ########### /Colect ###########

    ########### Train ###########
    # 변수 설정 --- ①
    dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "faces", name + "_" + id
    )
    train_data, train_labels = [], []

    print("Collecting train data set:")

    id = dir.split("_")[1]
    files = glob.glob(os.path.join(dir, "*.jpg"))
    print("\t path:%s, %dfiles" % (dir, len(files)))
    for file in files:
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        train_data.append(np.asarray(img, dtype=np.uint8))
        train_labels.append(int(id))

    train_data = np.asarray(train_data)
    train_labels = np.int32(train_labels)

    print("Starting LBP Model training...")
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(train_data, train_labels)
    model.write(dir + "all_face.xml")
    print("Model trained successfully!")

    ########### /Train ###########


if __name__ == "__main__":
    main(name="KGH1113", id="01")
