import streamlit as st
import cv2
import numpy as np
from sketch_utils import apply_sketch_effect, save_snapshot

# Set up the Streamlit page
st.set_page_config(page_title="Real-Time Sketch App", layout="centered")
st.title("🖼️ Real-Time Sketch Filter App")
st.write("Displays original and sketch output side-by-side.")

# UI elements for user interaction
start = st.checkbox("Start Camera")               # Checkbox to start/stop the camera
snapshot = st.button("📸 Save Snapshot")          # Button to save the current sketch frame
FRAME_WINDOW = st.image([])                       # Placeholder to display video frames

# Track snapshot requests using session state
if "save_requested" not in st.session_state:
    st.session_state.save_requested = False       # Initialize the save flag
if snapshot:
    st.session_state.save_requested = True        # Set flag when button is clicked

# When the user starts the camera
if start:
    cap = cv2.VideoCapture(0)                     # Access the webcam (device 0)
    st.info("Camera started. Uncheck the box to stop.")
    while True:
        ret, frame = cap.read()                   # Read a frame from the webcam
        if not ret:
            st.warning("Failed to grab frame.")
            break
        frame = cv2.resize(frame, (640, 480))     # Resize for consistent display
        sketch = apply_sketch_effect(frame)       # Apply the sketch effect
        sketch_bgr = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)# Convert sketch back to 3-channel image for side-by-side view
        combined = np.hstack((frame, sketch_bgr))#Combine original and sketch images side-by-side
        FRAME_WINDOW.image(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)) # Display the combined image in the app
        if st.session_state.save_requested: # Save snapshot if user requested
            save_snapshot(sketch)
            st.success("✅ Snapshot saved to 'Snapshot/' folder!")
            st.session_state.save_requested = False
        if not st.session_state.get("Start Camera", True): # Exit the loop if the checkbox is unchecked
            break
    cap.release()# Release the webcam and close any OpenCV windows
    cv2.destroyAllWindows()

else:
    st.info("✅ Click 'Start Camera' to begin.") # Message shown when camera is not active

