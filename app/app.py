import streamlit as st
from ultralytics import YOLO
import PIL
#import cv2
import matplotlib.pyplot as plt
#import ipywidgets as widgets
#from IPython.display import Image, display, clear_output
import numpy as np
#import glob
import os

st.title("Woodboard Counter v8.0")

# Load model
model_path = r'./model/last.pt'
model = YOLO(model_path)

# img = np.array(PIL.Image.open(List_img[0]))

# Define the path to the directory
directory_path = "./raw_images"

# Get a list of all files in the directory
file_list = os.listdir(directory_path)

def ratio(f,v_min, v_max, h_min, h_max):
        size_to_display = 501
        print(np.array(PIL.Image.open(f)).shape[1]//size_to_display )
        return np.array(PIL.Image.open(f)).shape[1]//size_to_display 
    
    
def plot_crop_lines(f,v_min, v_max, h_min, h_max):
        width = 5
        img_= (np.array(PIL.Image.open(directory_path+"/"+f)))
        img_[:, v_min-width:v_min+width, :] = [255, 0, 0]
        img_[:, v_max-width:v_max+width, :] = [255, 0, 0]
        img_[ h_min-width: h_min+width,: , :] = [255, 0, 0]
        img_[ h_max-width: h_max+width,: , :] = [255, 0, 0]
        im = img_[h_min:h_max, v_min:v_max, :]
        st.image(img_, use_column_width=True)
        return im


def show(results):
    for r in results:      
        fig, ax = plt.subplots(1,2,figsize=(14,5))
        im_array = r.plot(line_width=3)  # plot a BGR numpy array of predictions
        ax[0].imshow(im_array) #np.flip(im_array, axis=-1) to correct colors
        st.markdown(f"<h1 style='text-align: center; color: blue;'>Nombre de planches: {r.__len__()}</h1>", unsafe_allow_html=True)
        # On crée le np.array col0à3 coordonnées de la box, 4 et 5 milieu de chaque box, 6:confidence level
        coord = np.array(r.boxes.xyxy)
        coord = np.column_stack((coord, (coord[:,0]+coord[:,2])/2, (coord[:,1]+coord[:,3])/2, np.array(r.boxes.conf)))
        for i,c in enumerate(coord):
            ax[0].text(x=c[4], y=c[5], s=i)
        ax[1].plot(coord[:,6], marker='o')
        ax[1].set_xlabel('numéro de box')
        ax[1].set_ylabel('Confidence')
        ax[1].grid()

        st.pyplot(fig)

        
def count_board(conf, img_cropped):
    results = model.predict(source=img_cropped, # image_to_predict
                            show=False, 
                            conf=conf,
                            save=False, 
                            line_width=3,
                            project='Board_counter',
                            );
    show(results)


def main():

    with st.sidebar:
        col1, col2 = st.columns(2)
        with col1:
            st.image('./logo/logo_round.png', width = 100)
        with col2:
            st.image('./logo/logo_Simonin.png', width = 150)
        selected_file = st.selectbox("Select a file from ./raw_images", file_list)
        #
        size= (np.array(PIL.Image.open(directory_path+"/"+selected_file))).shape
        # st.write(size) # image size
        #
        vert_x_min = st.slider("Vert min:", min_value=0, max_value=size[1], value=100, step=25)
        vert_x_max = st.slider("Vert max:", min_value=0, max_value=size[1], value=2500, step=25)
        hori_y_min = st.slider("Hori min:", min_value=0, max_value=size[0], value=100, step=25)
        hori_y_max = st.slider("Hori max:", min_value=0, max_value=size[0], value=2500, step=25)
    
    im = plot_crop_lines(selected_file,vert_x_min, vert_x_max, hori_y_min, hori_y_max)
    with st.sidebar:
        conf= st.slider("Seuil de détection:", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
        button_clicked = st.button("Count")
    if button_clicked:
            count_board(conf,im)

if __name__=="__main__":
    main()