import streamlit as st
from PIL import Image
import subprocess

def generate_avatar(input_image_path):
    # Run Avatarify with the input image
    subprocess.run(['python', 'avatarify.py', '--image', input_image_path])

def main():
    st.title("AI-Generated Headshots with Avatarify")

    # File uploader for image input
    uploaded_file = st.file_uploader("Upload your headshot image", type=["jpg", "png"])

    if uploaded_file is not None:
        # Display uploaded image
        input_image = Image.open(uploaded_file)
        st.image(input_image, caption="Uploaded Image", use_column_width=True)

        # Generate avatar button
        if st.button("Generate Avatar"):
            # Save uploaded image to temporary file
            input_image_path = "input_image.jpg"
            input_image.save(input_image_path)

            # Generate avatar
            generate_avatar(input_image_path)

            # Display generated avatar
            generated_image = Image.open("avatar.jpg")
            st.image(generated_image, caption="Generated Avatar", use_column_width=True)

if __name__ == "__main__":
    main()
