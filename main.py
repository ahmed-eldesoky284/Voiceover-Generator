import streamlit as st
import requests
import io
from PIL import Image

def generate_headshots(image, num_images, image_quality):
    # Define the DALL-E API endpoint
    api_endpoint = "https://api.openai.com/v1/generators/davinci-codex/images"
    api_key = st.secrets['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']

    # Set additional parameters for DALL-E image generation
    params = {
        "prompt": "Generate professional LinkedIn headshot images.",
        "num_images": num_images,
        "image_quality": image_quality
    }

    # Set authorization headers with your API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        # Send a POST request to the DALL-E API
        response = requests.post(api_endpoint, json=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response JSON
        result = response.json()

        # Extract the generated image URLs
        image_urls = result.get("images")

        # Download and return the generated images
        generated_images = []
        for url in image_urls:
            image_data = requests.get(url).content
            img = Image.open(io.BytesIO(image_data))
            generated_images.append(img)

        return generated_images

    except requests.exceptions.RequestException as e:
        st.error(f"Error generating headshot images: {e}")
        return None

def main():
    st.title("AI-Generated Headshots")

    # Upload image
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        # Number of headshots to generate
        num_images = st.slider("Number of Headshots", min_value=1, max_value=10, value=5)

        # Image quality
        image_quality = st.slider("Image Quality", min_value=0.1, max_value=1.0, value=0.5, step=0.1)

        # Generate headshots button
        if st.button("Generate Headshots"):
            # Generate headshots
            generated_headshots = generate_headshots(uploaded_image, num_images, image_quality)

            if generated_headshots:
                # Display and save generated headshots
                for i, img in enumerate(generated_headshots, start=1):
                    st.image(img, caption=f"Generated Headshot {i}", use_column_width=True)
                    # Save the image
                    img.save(f"generated_headshot_{i}.png")

if __name__ == "__main__":
    main()
