import streamlit as st
from PIL import Image
import requests

# Left-aligned Title of the app with larger font size
st.markdown("""
    <style>
        .big-font {
            font-size: 48px;
            text-align: left;
        }
        .big-header {
            font-size: 36px;
        }
        .container {
            display: flex;
            justify-content: center;
        }
        .image-container {
            margin: 10px;
            padding: 10px;
        }
        .image {
            width: 100%; /* Adjust as needed */
        }
    </style>
    <h1 class="big-font">Prediction of RUL for Jet Engines</h1>
""", unsafe_allow_html=True)

# Sidebar for file upload
st.sidebar.header("Please upload your file!")
uploaded_file = st.sidebar.file_uploader("", type="txt")

jetengine_api_url = 'https://jetengine-rstitszjmq-ew.a.run.app/upload'

# Main area for displaying images
st.markdown('<h2 class="big-header">Engine Performance Details</h2>', unsafe_allow_html=True)

# Load images
image1 = Image.open("image1.png")  # Replace with actual image paths
image2 = Image.open("image2.png")  # Replace with actual image paths
image3 = Image.open("image3.png")  # Replace with actual image paths
image4 = Image.open("image4.png")  # Replace with actual image paths

# Display images based on file upload status
if uploaded_file is not None:
    # Display images when file is uploaded
    col1, col2 = st.columns([1, 1.5])  # Adjust column widths

    with col1:
        st.image(image2, use_column_width=True)
    with col2:
        st.image(image1, use_column_width=True)
        st.image(image3, use_column_width=True)

    # Process the uploaded file and get prediction
    files = {'file': uploaded_file}
    response = requests.post(jetengine_api_url, files=files)

    if response.status_code == 200:
        prediction = response.json()
        pred = prediction['RUL']
        st.header(f'The given jet engine has {pred} more cycles before failure')
    else:
        st.header('Error in prediction. Please try again.')
else:
    # Display image4 when no file is uploaded
    st.image(image4, use_column_width=True)
    st.header('No file uploaded yet.')

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
