import streamlit as st
from utils import detect_faces
import base64

st.set_page_config(page_title='All Same Face')

# Title
st.title("All Same Face")

st.write("Upload a picture with more than one person")
st.write("It may take more time if the picture has many faces..")

# Sidebar
st.sidebar.header("User Input")
user_input = st.sidebar.text_input("Enter your name", "John Doe")


# Show an image
image = st.file_uploader("Upload an image (jpg,jpeg,png)",type=['jpg', 'jpeg', 'png'])
if image is not None:
    st.image(image, caption="Uploaded Image", use_column_width=True)
    # detect faces 
    images = detect_faces(image)
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
    
    selected_option = st.selectbox("Select an option", options)
    if selected_option != 'choose target image':
        index = int(selected_option.split(' ')[-1]) -1
        st.image(images[index],caption=" image")
        