from __future__ import division, print_function
import os
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import tensorflow as tf
from skimage.transform import resize
import streamlit as st

# Apply custom CSS to style the app
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inline CSS for white and blue theme
def inject_custom_css():
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: white;
    }
    
    /* Title */
    h1 {
        color: #1E90FF;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }

    /* Uploader */
    .stFileUploader {
        border: 2px solid #1E90FF;
        border-radius: 10px;
        padding: 10px;
        background-color: #F0F8FF;
        color: #1E90FF;
        font-family: 'Arial', sans-serif;
        font-size: 16px;
    }

    /* Prediction text */
    .stMarkdown {
        text-align: center;
        font-size: 22px;
        color: #1E90FF;
        font-family: 'Arial', sans-serif;
    }

    /* Image style */
    img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border: 5px solid #1E90FF;
        border-radius: 10px;
    }

    /* Buttons */
    .stButton>button {
        color: white;
        background-color: #1E90FF;
        border: none;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #4682B4;
    }
    </style>
    """, unsafe_allow_html=True)

# Inject the custom CSS for the white and blue theme
inject_custom_css()

# Load the trained model (adjust the path to your environment)
MODEL_PATH = 'Skin_Diseases.h5'

# Load your trained model
@st.cache_resource
def load_model_cached():
    model = load_model(MODEL_PATH)
    return model

model = load_model_cached()

# Define the index for the classes
index = ['Acne', 'Melanoma', 'Psoriasis', 'Rosacea', 'Vitiligo']

# Main page title
st.title("Skin Disease Prediction")

# File uploader for the user to upload an image
uploaded_file = st.file_uploader("Upload an image of the skin condition", type=["jpg", "png", "jpeg"])

# Function to preprocess the image
def preprocess_image(file):
    img = image.load_img(file, target_size=(64, 64))  # Resize image
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)  # Expand dimensions to match model input
    return x

# Display prediction if an image is uploaded
if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
    # Preprocess the image
    img = preprocess_image(uploaded_file)

    # Predict the class of the uploaded image
    preds = model.predict(img)
    predicted_class = index[np.argmax(preds[0])]

    # Display the prediction
    st.markdown(f"**Prediction: {predicted_class}**")
