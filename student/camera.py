import os

import cv2
from django.conf import settings

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
    settings.BASE_DIR, 'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))


class VideoCamera(object):
    def __init__(self, user_id):
        self.video = cv2.VideoCapture(0)
        self.user_id = user_id

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_detected = face_detection_videocam.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h),
                          color=(255, 0, 0), thickness=2)
        frame_flip = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()


class TrainModel(object):
    def __init__(self, user_id):
        self.video = cv2.VideoCapture(1)
        self.user_id = user_id
        self.count = 1

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    # def saveImage(self, img):
    #     Path(f"dataset/{name}").mkdir(parents=True, exist_ok=True)
    #     cv2.imwrite(f"dataset/{name}/{id}_{imgId}.jpg", img)

    def get_frame(self):
        success, image = self.video.read()
        original_image = image

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_detected = face_detection_videocam.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(100,100))

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
            cords[1] : cords[1] + cords[3],
            cords[0] : cords[0] + cords[2]
        ]

        self.saveImage(updImg)

        frame_flip = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()
