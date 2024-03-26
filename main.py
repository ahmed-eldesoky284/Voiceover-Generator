import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

# Load pre-trained style transfer model
style_transfer_model = hub.load("https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")

# Function to apply style transfer to an image
def apply_style_transfer(image, style_image):
    # Resize style image to match content image size
    style_image = cv2.resize(style_image, (image.shape[1], image.shape[0]))
    # Convert to float32 and normalize pixel values
    content_image = tf.convert_to_tensor(image, tf.float32) / 255.0
    style_image = tf.convert_to_tensor(style_image, tf.float32) / 255.0
    # Apply style transfer
    stylized_image = style_transfer_model(tf.constant(content_image), tf.constant(style_image))[0]
    # Convert to numpy array and rescale pixel values
    stylized_image = (stylized_image.numpy() * 255).astype(np.uint8)
    return stylized_image

def main():
    st.title("Real-time Fashion Style Transfer")

    # Initialize video capture object
    cap = cv2.VideoCapture(0)

    # Load fashion image
    fashion_image_path = "fashion_image.jpg"
    fashion_image = cv2.imread(fashion_image_path)

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret:
            # Apply style transfer using fashion image style to the captured frame
            stylized_frame = apply_style_transfer(frame, fashion_image)
            
            # Display the original and stylized frames
            st.image([frame, stylized_frame], caption=["Original Frame", "Stylized Frame"], width=300)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()

if __name__ == "__main__":
    main()
