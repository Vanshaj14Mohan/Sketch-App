import cv2
import os
from datetime import datetime

# Applies a pencil sketch effect to a given BGR image
def apply_sketch_effect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Convert the image to grayscale
    inv = 255 - gray #Invert the grayscale image (white becomes black, black becomes white)
    blur = cv2.GaussianBlur(inv, (21, 21), 0)# Invert the grayscale image (white becomes black, black becomes white)
    sketch = cv2.divide(gray, 255 - blur, scale=256)  #Blend the grayscale image with the blurred inverted image to get a sketch effect
    return sketch

# Saves the sketch image to a folder with a timestamped filename
def save_snapshot(image, folder="Snapshot"):
    # Create the output folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate a unique filename using current date and time
    filename = f"sketch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(folder, filename)

    # Save the image to disk
    cv2.imwrite(filepath, image)
    return filepath  # Return the full path of the saved image
