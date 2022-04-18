import os

import cv2
from django.conf import settings

from student.models import Student as sdb

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
    settings.BASE_DIR, 'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

static_dir = os.path.join(settings.BASE_DIR, 'static')
student_dir = os.path.join(static_dir, 'profile_pic', 'Student')


class VideoCamera(object):
    def __init__(self, student):
        self.video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.video.set(cv2.CAP_PROP_FPS, 12)
        self.student = student
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        imgPath = os.path.join(student_dir, str(student.user_id))
        training_file = os.path.join(imgPath, "training.yml")
        self.recognizer.read(training_file)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        success, image = self.video.read()
        image = cv2.flip(image, 1)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_detected = face_detection_videocam.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h),
                          color=(255, 0, 0), thickness=2)
            pid, percentage = self.recognizer.predict(gray[y:y+h, x:x+w])

            name = 'unknown'
            if pid == self.student.user_id:
                name = self.student.get_name
            
            if(name is not 'unknown' and percentage >= 80):
                percentage = round(percentage)
                cv2.putText(
                    image, name, (x, h+y-4),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1, (0, 0, 255), 2
                )

                cv2.putText(image, 'predict: ' + str(percentage) + '%',
                    (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            else:
                percentage = round(percentage)
                cv2.putText(
                    image, 'Unknown', (x, h+y-4),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1, (0, 0, 255), 2
                )

                cv2.putText(image, 'predict: ' + str(percentage) + '%',
                    (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class TrainModel(object):
    def __init__(self, student):
        self.video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.student = student
        self.count = 1

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def saveImage(self, img):
        imgPath = os.path.join(
            static_dir,
            "profile_pic",
            "Student",
            f"{self.student.user_id}"
        )

        cv2.imwrite(f"{imgPath}/{self.student.user_id}_{self.count}.jpg", img)
        self.count += 1

    def get_frame(self):
        success, image = self.video.read()
        original_image = image

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_detected = face_detection_videocam.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

        cords = [0, 0, 0, 0]
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(
                image,
                pt1=(x, y),
                pt2=(x + w, y + h),
                color=(255, 0, 0),
                thickness=2
            )

            cords = [x, y, w, h]

        updImg = original_image[
            cords[1]: cords[1] + cords[3],
            cords[0]: cords[0] + cords[2]
        ]

        if(cords[2] >= 100 and cords[3] >= 100 and self.count <= 20):
            self.saveImage(updImg)

        if(self.count > 20):
            sdb.objects.update_or_create(
                user_id=self.student.user_id,
                defaults={
                    'is_trained': 'True'
                }
            )

        frame_flip = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()
