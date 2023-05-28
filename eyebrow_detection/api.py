from typing import List, Tuple
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import csv
import cv2
import dlib
import imutils
from imutils import face_utils
import numpy as np
import io

face_detector = dlib.get_frontal_face_detector()
predictor_path = "./eyebrow_detection/model.dat"
landmark_detector = dlib.shape_predictor(predictor_path)

def detect_face(img: np.array) -> List[Tuple[int, int]]:
    face = face_detector(img, 1)
    landmark_tuple = []
    for k, d in enumerate(face):
        landmarks = landmark_detector(img, d)
        for n in range(17, 27):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmark_tuple.append((x, y))
    return landmark_tuple

async def create_upload_file(files: List[UploadFile] = File(...)):
    rows = []
    rows.append(', '.join(["Image_ID", "Landmark_Number", "X", "Y", "Eyebrow"]))

    for file in files:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        landmarks = detect_face(img)
        landmark_num = 1
        for i in range(10):
            eyebrow = "L"
            if landmark_num > 5:
                eyebrow = "R"
            rows.append(
                ', '.join([file.filename, str(landmark_num), str(landmarks[i][0]), str(landmarks[i][1]), eyebrow])

                    )
            landmark_num += 1
    return rows
