import insightface 
import cv2
import numpy as np
from insightface.app import FaceAnalysis

def main():
    return;

def detect_faces(img):
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640,640))
    file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    faces = app.get(img)
    data = []
    for face in faces:
        bbox=face['bbox']
        bbox = [int(b) for b in bbox]
        clipped_face = img[bbox[1]:bbox[3], bbox[0]:bbox[2], ::-1]
        data.append(clipped_face)
    return data,img,faces

def load_model():
    swapper = insightface.model_zoo.get_model('inswapper_128.onnx',download=False,download_zip=False)
    return swapper
def swap_face(img,faces,target_face,swapper):
    res = img.copy()
    for face in faces:
        res = swapper.get(res,face,target_face,paste_back=True)
    return res[:,:,::-1]


if __name__ == "__main__":
    main()