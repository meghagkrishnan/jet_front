import streamlit as st
from PIL import Image
import pandas as pd
import requests

# Title of the app
st.title('Prediction of RUL for Jet Engines')

# Display the heading image
heading_image = Image.open("image.png")

st.image(heading_image, use_column_width=True)

uploaded_file = st.file_uploader("Choose a text file", type="txt")

jetengine_api_url = 'https://jetengine-rstitszjmq-ew.a.run.app/upload'



if uploaded_file is not None:
    # Read the data from the text file
    files = {'file':uploaded_file}
    response = requests.post(jetengine_api_url, files = files)

    prediction = response.json()
    print (prediction)
    pred = prediction['RUL']

    st.header(f'The given jet engine has {pred} more cycles before failure')

else:

    st.header('System Failure')
