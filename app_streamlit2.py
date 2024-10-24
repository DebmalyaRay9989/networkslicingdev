


import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px

# Load the model once when the app starts
@st.cache_resource
def load_model():
    return pickle.load(open('telecom.pkl', 'rb'))

model = load_model()

# Function to convert time to minutes
def time_to_minutes(time_value):
    """Convert a time input to total minutes."""
    return time_value.hour * 60 + time_value.minute

# Title of the app
st.title("📶 Telecom Category Prediction")

# Instructions for the user
st.markdown("""
    Please fill in the details below to predict the telecom category. 
    Ensure that all fields are filled correctly for accurate predictions.
""")

st.markdown("""
    <style>
    .sidebar .sidebar-content {
        padding: 10px;
    }
    .sidebar {
        background-color: #f8f9fa; /* Light gray sidebar background */
    }

    /* Sidebar Button Styling */
    .sidebar .stButton {
        background-color: #007bff; /* Bootstrap blue color */
        color: white;               /* White text for contrast */
        padding: 10px 20px;        /* Adequate padding */
        border: none;              /* No border */
        border-radius: 4px;       /* Slightly rounded corners */
        font-size: 16px;           /* Font size for better readability */
        font-weight: bold;         /* Bold text for emphasis */
        cursor: pointer;           /* Pointer cursor on hover */
        transition: background-color 0.3s, transform 0.2s; /* Smooth transitions */
        margin: 5px 0;            /* Margin for spacing between buttons */
    }

    /* Hover State */
    .sidebar .stButton:hover {
        background-color: #0056b3; /* Darker blue on hover */
        transform: translateY(-1px); /* Lift effect */
    }

    /* Active State */
    .sidebar .stButton:active {
        background-color: #004085; /* Even darker blue when active */
        transform: translateY(1px); /* Slight press down effect */
    }

    h1, h2, h3 {
        color: #333;                /* Header text color */
        font-family: 'Arial', sans-serif; /* Font family */
    }
    h1 {
        font-size: 2em; 
        font-weight: bold;
    }
    h2 {
        font-size: 1.5em; 
    }
    h3 {
        font-size: 1.2em; 
    }

    input, select {
        border-radius: 5px;         /* Round corners */
        border: 1px solid #ccc;      /* Light gray border */
        padding: 5px;                /* Padding */
        width: 100%;                 /* Full width */
        transition: border-color 0.2s; /* Transition for focus */
    }
    input:focus, select:focus {
        border-color: #66afe9; /* Change border color when focused */
        box-shadow: 0 0 5px rgba(102, 175, 233, .5); /* Light blue shadow */
    }

    .stError {
        color: #ff4d4d; /* Bright red for error messages */
        font-weight: bold; /* Make it bold */
    }

    .main {
        padding: 20px; /* Add padding around the main content area */
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar for input fields using tabs
st.sidebar.header("Input Parameters")
tab1, tab2 = st.sidebar.tabs(["General Inputs", "Advanced Inputs"])

# General Inputs Tab
with tab1:
    lte_5g_category = st.selectbox("LTE 5G Category", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    time_value = st.time_input("Select Time", value=pd.Timestamp.now().time())  # Default to current time
    
    packet_loss_rate = st.number_input("Packet Loss Rate (0.00 - 1.00)", format="%.2f", min_value=0.0, max_value=1.0, step=0.01)
    packet_delay = st.number_input("Packet Delay (ms)", min_value=0, step=1)
    
# Advanced Inputs Tab
with tab2:
    io_t = st.number_input("IoT (0 - 100)", min_value=0, max_value=100, step=1)
    lte_5g = st.number_input("LTE 5G (0 - 100)", min_value=0, max_value=100, step=1)
    gbr = st.number_input("GBR (0 - 100)", min_value=0, max_value=100, step=1)
    non_gbr = st.number_input("Non-GBR (0 - 100)", min_value=0, max_value=100, step=1)
    ar_vr_gaming = st.number_input("AR/VR Gaming (0 - 100)", min_value=0, max_value=100, step=1)
    healthcare = st.number_input("Healthcare (0 - 100)", min_value=0, max_value=100, step=1)
    industry_4_0 = st.number_input("Industry 4.0 (0 - 100)", min_value=0, max_value=100, step=1)
    io_t_devices = st.number_input("IoT Devices (0 - 100)", min_value=0, max_value=100, step=1)
    public_safety = st.number_input("Public Safety (0 - 100)", min_value=0, max_value=100, step=1)
    smart_city_and_home = st.number_input("Smart City and Home (0 - 100)", min_value=0, max_value=100, step=1)
    smart_transportation = st.number_input("Smart Transportation (0 - 100)", min_value=0, max_value=100, step=1)
    smartphone = st.number_input("Smartphone (0 - 100)", min_value=0, max_value=100, step=1)

# Button to predict
if st.sidebar.button("Predict"):
    # Validate inputs
    if time_value is None:
        st.error("Please select a valid time.")
    else:
        time_in_minutes = time_to_minutes(time_value)
        
        # Prepare input data for prediction
        input_data = np.array([[lte_5g_category, time_in_minutes, packet_loss_rate, packet_delay, io_t, lte_5g,
                                gbr, non_gbr, ar_vr_gaming, healthcare, industry_4_0, io_t_devices,
                                public_safety, smart_city_and_home, smart_transportation, smartphone]])
        
        # Make prediction
        prediction = model.predict(input_data)
        output = int(prediction)

        # Display prediction result
        st.success(f"It is predicted as category: **{output}**")

        # Display input data as a DataFrame
        input_df = pd.DataFrame(input_data, columns=["LTE 5G Category", "Time (minutes)", "Packet Loss Rate", 
                                                      "Packet Delay", "IoT", "LTE 5G", "GBR", "Non-GBR", 
                                                      "AR/VR Gaming", "Healthcare", "Industry 4.0", 
                                                      "IoT Devices", "Public Safety", "Smart City", 
                                                      "Smart Transportation", "Smartphone"])
        
        st.subheader("Input Parameters DataFrame")
        st.dataframe(input_df)

        # Visualization of input parameters using Plotly
        st.subheader("Input Parameters Visualization")
        input_df_melted = input_df.melt(var_name='Parameter', value_name='Value')
        
        fig = px.bar(input_df_melted, x='Parameter', y='Value', title='Input Parameters',
                      labels={'Value': 'Values', 'Parameter': 'Parameters'},
                      color='Parameter')
        st.plotly_chart(fig)

        # Additional Information
        st.markdown("### Additional Information")
        st.json({
            "LTE 5G Category": lte_5g_category,
            "Time (minutes)": time_in_minutes,
            "Packet Loss Rate": packet_loss_rate,
            "Packet Delay (ms)": packet_delay,
            "IoT": io_t,
            "LTE 5G": lte_5g,
            "GBR": gbr,
            "Non-GBR": non_gbr,
            "AR/VR Gaming": ar_vr_gaming,
            "Healthcare": healthcare,
            "Industry 4.0": industry_4_0,
            "IoT Devices": io_t_devices,
            "Public Safety": public_safety,
            "Smart City and Home": smart_city_and_home,
            "Smart Transportation": smart_transportation,
            "Smartphone": smartphone
        })

        # Optional: Button to download input data as CSV
        csv = input_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Input Data as CSV", csv, "input_data.csv", "text/csv")












