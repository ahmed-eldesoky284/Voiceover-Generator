
       

import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

def generate_images(prompt, size, quality, n):
    try:
        # Generate images using OpenAI API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=n
        )
        return response["images"]
    except Exception as e:
        st.error(f"Error generating images: {e}")
        return None
def edit_images(image_path, mask_path, prompt, num_images=1, size="1024x1024"):
    # Use the OpenAI client to edit images
    response = client.images.edit(
        image=open(image_path, "rb"),
        mask=open(mask_path, "rb"),
        prompt=prompt,
        n=num_images,
        size=size
    )
    return response
def main():
    st.title("DALL-E Image Generator")
    
    # User input for prompt, size, quality, and number of images
    prompt = st.text_input("Enter prompt", "a white siamese cat")
    size = st.selectbox("Image size", ["512x512", "1024x1024"])
    quality = st.selectbox("Image quality", ["standard", "high"])
    n_images = st.slider("Number of images", min_value=1, max_value=5, value=1)
    
    # Generate images button
    if st.button("Generate Images"):
        # Generate images
        images = generate_images(prompt, size, quality, n_images)
        
        if images:
            # Display generated images
            for i, img in enumerate(images, start=1):
                st.image(img, caption=f"Generated Image {i}", use_column_width=True)

if __name__ == "__main__":
    main()



