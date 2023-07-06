import streamlit as st
from utils import detect_faces, swap_face,load_model
import cv2
import base64
from io import BytesIO
from PIL import Image

def convert_image(img):
    pil_image = Image.fromarray(img)
    buf = BytesIO()
    pil_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

st.set_page_config(page_title='All Same Face')

# Title
st.title("All Same Face")

st.write("Upload a picture with more than one person")
st.write("It may take more time if the picture has many faces..")


# Show an image
image = st.file_uploader("Upload an image (jpg,jpeg,png)",type=['jpg', 'jpeg', 'png'])
if image is not None:
    st.image(image, caption="Uploaded Image", use_column_width=True)
    # get file name for the new image
    file_name = image.name
    # detect faces 
    images,img,faces = detect_faces(image)
    col1,col2,col3,col4 = st.columns(4)
    options=['choose target image']
    for i,clippedimage in enumerate(images):
        i = i+1
        options.append(f"clipped-face {i}")
        index = i % 4
        if index==1:
            col1.image(clippedimage,caption=f"clipped-face {i}")
        if index==2:
            col2.image(clippedimage,caption=f"clipped-face {i}")
        if index==3:
            col3.image(clippedimage,caption=f"clipped-face {i}")
        if index==0:
            col4.image(clippedimage,caption=f"clipped-face {i}")
    if (model :=load_model()):
       selected_option = st.selectbox("Select an option", options)
       if selected_option != 'choose target image':
            index = int(selected_option.split(' ')[-1]) -1
            st.image(images[index],caption="target face")
            new_image = swap_face(img,faces,faces[index],model)
            st.image(new_image,caption='All Same Face')
            
            st.download_button("Download Swapped Image", convert_image(new_image),f"swapped_{file_name.split('.')[0]}.png","image/png")
            
    else:
        st.write("Loading trained model")

        