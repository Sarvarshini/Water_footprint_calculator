import streamlit as st
import requests
from PIL import Image
import io

# Define the URL of your Flask API
API_URL = 'http://127.0.0.1:5000/predict'

st.title("Water Footprint Calculator")

# Allow users to upload an image
uploaded_file = st.file_uploader("Upload an image of a vegetable", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_container_width=True)

    # Convert image to bytes for sending to API
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Add a button to make a prediction
    if st.button('Predict'):
        with st.spinner('Classifying...'):
            try:
                # Send the image to Flask API
                response = requests.post(API_URL, files={"file": buffer})
                data = response.json()

                # Display the results
                if "predicted_class" in data:
                    st.success(f"**Prediction:** {data['predicted_class']}")
                    st.markdown(f"**Water Footprint Info:** {data['footprint_info']}")
                else:
                    st.error("Error: Unable to get prediction.")
            except Exception as e:
                st.error(f"Error: {e}")
