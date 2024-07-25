import streamlit as st
from PIL import Image
import requests
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')

# Styling
st.markdown("""
    <style>
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #788FCD !important;
        }
        /* Main content styling */
        .container {
            display: flex;
            align-items: center;
            height: 100vh; /* Full viewport height */
        }
        .column {
            display: flex;
            flex-direction: column;
            justify-content: flex-start; /* Start at the top */
            height: 100%; /* Make sure the column fills the available height */
            padding-top: 100px; /* Add padding at the top */
        }
        .status-box {
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            font-size: 24px;
            color: black;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .critical {
            background-color: #ff6666;
        }
        .warning {
            background-color: #ffcc00;
        }
        .normal {
            background-color: #085C37;
        }
        .prediction {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px; /* Add some space below the prediction text */
        }
        .prediction-critical {
            color: #ff6666;
        }
        .prediction-warning {
            color: #ffcc00;
        }
        .prediction-normal {
            color: #085C37;
        }
        .small-header {
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            margin-bottom: -5px; /* Reduce space below the header */
            margin-top: -5px;  /* Reduce space above the header */
        }
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center; /* Center align text and image */
            text-align: center; /* Center align text */
            margin-left: 20px; /* Adjust margin if needed */
        }
        .welcome-text {
            margin-bottom: 0; /* Remove margin between text and image */
        }
        .welcome-image {
            max-width: 700px; /* Ensure the image is larger */
            width: 100%;
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for file upload
st.sidebar.header("Please upload your file!")
uploaded_file = st.sidebar.file_uploader("", type="txt")

jetengine_api_url = 'https://jetengine-rstitszjmq-ew.a.run.app/predictLSTM'

# Create columns
col1, col2 = st.columns([2, 4])  # Adjust column widths after removing the first column

# Display content based on file upload status
if uploaded_file is not None:
    with col1:
        # Center content vertically in the column
        st.markdown('<div class="column">', unsafe_allow_html=True)

        # Process the uploaded file and get prediction
        files = {'file': uploaded_file}
        response = requests.post(jetengine_api_url, files=files)

        if response.status_code == 200:
            prediction = response.json()
            pred = round(prediction['RUL'])  # Round the RUL to the nearest whole number

            # Determine engine status and prediction color
            if pred < 30:
                status = "Critical Engine"
                status_class = "critical"
                prediction_class = "prediction-critical"
                donut_color = "#ff6666"
                donut_values = [10, 90]  # Red section 10%, remaining 90%
                image_sensor = "image_sensor_100.png"
                image_box = "image_box_100.png"
            elif 30 <= pred <= 60:
                status = "Warning Engine"
                status_class = "warning"
                prediction_class = "prediction-warning"
                donut_color = "#ffcc00"
                donut_values = [29, 71]  # Orange section 29%, remaining 71%
                image_sensor = "image_sensor_3.png"
                image_box = "image_box_3.png"
            else:
                status = "Normal Engine"
                status_class = "normal"
                prediction_class = "prediction-normal"
                donut_color = "#085C37"
                donut_values = [62, 38]  # Green section 62%, remaining 38%
                image_sensor = "image_sensor_99.png"
                image_box = "image_box_99.png"

            # Display engine status
            st.markdown(f"""
                <div class="status-box {status_class}">
                    {status}
                </div>
            """, unsafe_allow_html=True)

            # Display prediction with color
            st.markdown(f"""
                <div class="prediction {prediction_class}">
                    Cycles before Failure: {pred}
                </div>
            """, unsafe_allow_html=True)

            # Add a small header above the donut
            st.markdown(f"""
                <div class="small-header">
                    Left Percent:
                </div>
            """, unsafe_allow_html=True)

            # Create a smaller donut chart with no background
            fig, ax = plt.subplots(figsize=(2, 2))  # Smaller size
            size = 0.3
            colors = [donut_color, "#dddddd"]

            ax.pie(donut_values, radius=1, colors=colors, wedgeprops=dict(width=size, edgecolor='w'))
            ax.text(0, 0, f"{donut_values[0]}%", ha='center', va='center', fontsize=16, fontweight='bold', color=donut_color)  # Adjusted font size

            # Remove background
            fig.patch.set_alpha(0)
            ax.patch.set_alpha(0)

            st.pyplot(fig)

        else:
            st.header('Error in prediction. Please try again.')

        # Close the container
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Display images when file is uploaded
        st.image(image_sensor, use_column_width=True)
        st.image(image_box, use_column_width=True)
else:
    # Display message when no file is uploaded
    st.markdown("""
        <div class="welcome-container">
            <h1 class="welcome-text">Welcome to EngineVision!</h1>
            <h3 class="welcome-text">You will soon see your Engine Details here...</h3>
        </div>
    """, unsafe_allow_html=True)
    # Display the image
    image_path = "1.png"  # Ensure this is the correct path to your image
    image = Image.open(image_path)
    st.image(image, use_column_width=True, output_format='PNG')

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
