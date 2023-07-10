import insightface 
import cv2
import numpy as np
import warnings
warnings.filterwarning('ignore')
import os
import boto3
from insightface.app import FaceAnalysis
access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
default_region = os.environ.get('AWS_DEFAULT_REGION')

# override original package for some error 
def lstsq_with_rcond(X, Y):
    return np.linalg.lstsq(X, Y, rcond=None)[0]
insightface.utils.transform.lstsq = lstsq_with_rcond

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
    s3 = boto3.client('s3', 
                   aws_access_key_id=access_key_id, 
                   aws_secret_access_key=secret_access_key,
                   region_name=default_region)
    if not os.path.exists('inswapper_128.onnx'):
        s3.download_file('my-faceswapping-bucket', 'inswapper_128.onnx', 'inswapper_128.onnx')
    swapper = insightface.model_zoo.get_model('inswapper_128.onnx',download=False,download_zip=False)
    return swapper
def swap_face(img,faces,target_face,swapper):
    res = img.copy()
    for face in faces:
        res = swapper.get(res,face,target_face,paste_back=True)
    return res[:,:,::-1]


if __name__ == "__main__":
    main()