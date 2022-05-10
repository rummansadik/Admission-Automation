import os

import cv2 as cv
import face_recognition as fr
from django.conf import settings

from student.train_image import *
from student.models import Student as sdb


static_dir = os.path.join(settings.BASE_DIR, 'static')
student_dir = os.path.join(static_dir, 'profile_pic', 'Student')


class CheckCamera(object):
    def __init__(self, student):
        self.video = cv.VideoCapture(1, cv.CAP_DSHOW)
        self.video.set(cv.CAP_PROP_FPS, 10)
        self.student = student

        self.faces = get_encoded_faces(student.user_id)
        self.faces_encoded = list(self.faces.values())
        self.known_faces_user_id = list(self.faces.keys())

    def __del__(self):
        self.video.release()
        cv.destroyAllWindows()

    def train_update(self):
        sdb.objects.update_or_create(
            user_id=self.student.user_id,
            defaults={
                'is_trained': 'True'
            }
        )

    def get_frame(self):
        success, image = self.video.read()
        image = cv.flip(image, 1)
        face_locations = fr.face_locations(image)
        unknown_face_encodings = fr.face_encodings(image, face_locations)

        face_names = []
        for face_encodings in unknown_face_encodings:
            matches = fr.compare_faces(self.faces_encoded, face_encodings)
            name = 'unknown'
            face_distances = fr.face_distance(
                self.faces_encoded, face_encodings)
            index = np.argmin(face_distances)
            if matches[index]:
                print(matches)
                name = self.student.get_name
                self.train_update()
            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv.putText(
                image, name, (left-20, bottom+15),
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()
