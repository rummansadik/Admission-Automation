import os

import cv2 as cv
import face_recognition as fr
import numpy as np

from django.conf import settings

def encode_image(img_dir):
    print(img_dir)
    face = fr.load_image_file(img_dir)
    encoding = fr.face_encodings(face)
    print(type(encoding))
    print(len(encoding))

