import os

import cv2 as cv
from django.conf import settings

face_detection_videocam = cv.CascadeClassifier(os.path.join(
    settings.BASE_DIR, 'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

static_dir = os.path.join(settings.BASE_DIR, 'static')
student_dir = os.path.join(static_dir, 'profile_pic', 'Student')


class VideoCamera(object):
    def __init__(self, student):
        self.video = cv.VideoCapture(1, cv.CAP_DSHOW)
        self.video.set(cv.CAP_PROP_FPS, 12)
        self.student = student
        self.recognizer = cv.face.LBPHFaceRecognizer_create()
        imgPath = os.path.join(student_dir, str(student.user_id))
        training_file = os.path.join(imgPath, "training.yml")
        self.recognizer.read(training_file)

    def __del__(self):
        self.video.release()
        cv.destroyAllWindows()

    def get_frame(self):
        success, image = self.video.read()
        image = cv.flip(image, 1)

        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)

        faces_detected = face_detection_videocam.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))
        
        if len(faces_detected) == 1:
            for (x, y, w, h) in faces_detected:
                cv.rectangle(image, pt1=(x, y), pt2=(x + w, y + h),
                            color=(255, 0, 0), thickness=2)
                pid, percentage = self.recognizer.predict(gray[y:y+h, x:x+w])

                name = 'unknown'
                if (pid is self.student.user_id):
                    name = self.student.get_name

                percentage = round(percentage)
                cv.putText(
                    image, name, (x, h+y-4),
                    cv.FONT_HERSHEY_DUPLEX,
                    1, (0, 0, 255), 2
                )

                if((name is not 'unknown') and (percentage >= 80)):
                    cv.putText(image, 'predict: ' + str(percentage) + '%',
                                (25, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv.putText(image, 'predict: ' + str(percentage) + '%',
                                (25, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()
