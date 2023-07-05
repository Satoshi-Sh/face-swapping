import insightface 
import cv2
import numpy as np
from insightface.app import FaceAnalysis

def main():
    return;
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_size=(640,640))

def detect_faces(img):
    file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    faces = app.get(img)
    data = []
    for face in faces:
        bbox=face['bbox']
        bbox = [int(b) for b in bbox]
        clipped_face = img[bbox[1]:bbox[3], bbox[0]:bbox[2], ::-1]
        data.append(clipped_face)
    return data 

if __name__ == "__main__":
    main()