import streamlit as st
import requests
import io
from PIL import Image

def generate_headshots(num_images=5, image_size=(1024, 1024)):
    # Define the DALL-E API endpoint
    api_endpoint = "https://api.openai.com/v1/images"

    # Set your OpenAI API key
    api_key = "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"

    # Define the prompt for generating headshots
    prompt = "Generate professional LinkedIn headshot images."

    # Set additional parameters for DALL-E image generation
    params = {
        "prompt": prompt,
        "num_images": num_images,
        "image_size": image_size
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
            image = Image.open(io.BytesIO(image_data))
            generated_images.append(image)

        return generated_images

    except Exception as e:
        st.error(f"Error generating headshot images: {e}")

def main():
    # Set Streamlit app title
    st.title("AI Generated LinkedIn Headshots")

    # Add a sidebar with options
    num_images = st.sidebar.number_input("Number of Images", min_value=1, max_value=10, value=5)
    image_size = st.sidebar.slider("Image Size", min_value=256, max_value=2048
