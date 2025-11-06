"""
This module is responsible for detecting human faces within a given dataset,
which may include both images and videos.
"""

import opencv, sys, dlib as cv2

def detect_faces(path):
    face_detector= dlib.cnn_face_detection_model_v1('dlib_models/mmod_human_face_detector.dat')
    