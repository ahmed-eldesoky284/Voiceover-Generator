from io import BytesIO
import streamlit as st
import qrcode
import base64
import requests
from bs4 import BeautifulSoup
from PIL import Image

# Global variable to keep track of the number of QR codes generated
qr_code_count = 0

# Function to generate and display a QR code
def generate_qr_code(data):
    global qr_code_count
    qr_code_count += 1

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert PIL Image to bytes-like object
    img_byte_array = BytesIO()
    qr_img.save(img_byte_array, format="PNG")
    img_bytes = img_byte_array.getvalue()

    # Display QR code
    st.image(img_bytes, caption=f"QR Code {qr_code_count}", use_column_width=True)

    # Add button to download the generated QR code
    st.markdown(get_download_link(img_bytes, f"custom_qr_code_{qr_code_count}.png"), unsafe_allow_html=True)

# Function to generate download link for the QR code
def get_download_link(file_content, file_name):
    b64 = base64.b64encode(file_content).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{file_name}">Download QR Code {qr_code_count}</a>'
    return href

# Function to fetch logo image URL from social media URL
def fetch_logo_from_url(social_media_url):
    try:
        response = requests.get(social_media_url)
        soup = BeautifulSoup(response.content, "html.parser")
        logo_url = None

        # Logic to extract logo URL from the webpage
        # This would depend on the structure of the webpage and where the logo is located

        return logo_url
    except Exception as e:
        st.error(f"Error fetching logo: {e}")
        return None

# Function to generate custom QR code with a logo
def QR_code_design(data, logo, qr_color="black", background_color="white", border_color="black"):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=qr_color, back_color=background_color)

    # Open and resize logo image
    with Image.open(logo) as logo_img:
        logo_img = logo_img.resize((80, 80))  # Adjust size as needed

    # Calculate position to paste logo on QR code
    qr_width, qr_height = qr_img.size
    logo_width, logo_height = logo_img.size
    position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

    # Paste logo on QR code
    qr_img.paste(logo_img, position)

    # Convert PIL Image to bytes-like object
    img_byte_array = BytesIO()
    qr_img.save(img_byte_array, format="PNG")
    img_bytes = img_byte_array.getvalue()

    # Display QR code with logo
    st.image(qr_img, caption="Custom QR Code", use_column_width=True)

    # Add button to download the generated QR code
    st.markdown(get_download_link(img_bytes, "custom_qr_code.png"), unsafe_allow_html=True)

# Main function
def main():
    st.title("QR Code Generator")

    # Select number of images
    num_images = st.number_input("Enter the number of images", value=1, min_value=1, step=1)

    for i in range(num_images):
        # Select QR code type
        qr_type = st.selectbox(f"Select QR Code Type for Image {i+1}", ["WiFi", "Email", "Phone Call", "SMS", "Social Media", "Audio", "Video", "Image", "PPTX", "QRcode design"])

        if st.button(f"Generate QR Code for Image {i+1}"):
            if qr_type == "WiFi":
                ssid = st.text_input("Enter WiFi SSID")
                password = st.text_input("Enter WiFi Password", type="password")
                wifi_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
                generate_qr_code(wifi_data)
            
            elif qr_type == "Email":
                email = st.text_input("Enter Email Address")
                subject = st.text_input("Enter Email Subject")
                body = st.text_area("Enter Email Body")
                email_data = f"mailto:{email}?subject={subject}&body={body}"
                generate_qr_code(email_data)
            
            elif qr_type == "Phone Call":
                phone_number = st.text_input("Enter Phone Number")
                phone_call_data = f"tel:{phone_number}"
                generate_qr_code(phone_call_data)
                
            elif qr_type == "QRcode design":
                st.title("Custom QR Code Generator with Logo")

                # User inputs
                data = st.text_input("Enter data for QR code")
                logo = st.file_uploader("Upload logo image (PNG or JPEG)", type=["png", "jpg", "jpeg"])

                if st.button("Generate Custom QR Code"):
                    if data:
                        if logo:
                            QR_code_design(data, logo)
                        else:
                            st.warning("Please upload a logo image.")
                    else:
                        st.warning("Please enter data for the QR code.")
            
            elif qr_type == "Social Media":
                st.title("QR Code Generator")

                # Input field for social media URL
                social_media_url = st.text_input("Enter Social Media URL")

                if st.button("Generate QR Code"):
                    if social_media_url:
                        # Fetch the logo URL from the social media URL
                        logo_url = fetch_logo_from_url(social_media_url)

                        if logo_url:
                            # Download the logo image
                            logo_content = requests.get(logo_url).content

                            # Generate QR code using the logo image
                            QR_code_design(social_media_url, BytesIO(logo_content))
                        else:
                            st.warning("Logo not found on the provided URL.")
                    else:
                        st.warning("Please enter the Social Media URL.")
            
            elif qr_type == "Audio":
                audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])
                if audio_file is not None:
                    generate_qr_code(audio_file.getvalue())
            
            elif qr_type == "Video":
                video_file = st.file_uploader("Upload Video File", type=["mp4"])
                if video_file is not None:
                    generate_qr_code(video_file.getvalue())
            
            elif qr_type == "Image":
                image_file = st.file_uploader("Upload Image File", type=["jpg", "png"])
                if image_file is not None:
                    generate_qr_code(image_file.getvalue())
            
            elif qr_type == "PPTX":
                pptx_file = st.file_uploader("Upload PowerPoint File", type=["pptx"])
                if pptx_file is not None:
                    generate_qr_code(pptx_file.getvalue())

if __name__ == "__main__":
    main()
               
               
