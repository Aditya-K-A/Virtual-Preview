import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# Helper functions for image handling
def image_to_base64(image):
    return base64.b64encode(image.read()).decode("utf-8")

def decode_base64_to_image(base64_data):
    return Image.open(BytesIO(base64.b64decode(base64_data)))

# Function to call the Text-to-Image API
def generate_outfits(prompt, api_key):
    url = "https://api.segmind.com/v1/stable-diffusion-3.5-large-txt2img"
    headers = {"x-api-key": st.secrets["API"]["api_key"]}
    data = {
        "prompt": prompt,
        # "negative_prompt": "low quality, blurry, cropped head, disfigured face, animated",
        "negative_prompt": '''Blurry details, incomplete outfit, disproportionate body shape, overly bright or unnatural lighting, unrealistic or overly exaggerated features, 
         distracting backgrounds, mismatched accessories, poorly styled or irrelevant attire, inconsistent textures, or low-quality rendering''',
        "steps": 50,  # Increased for better quality
        "guidance_scale": 7.5,  # Increased to emphasize prompt details
        "seed": 98552302,
        "sampler": "euler",
        "scheduler": "sgm_uniform",
        "width": 768,  # Adjusted dimensions for better proportions
        "height": 1024,  # Ensures full-body images with heads
        "batch_size": 4,
        "image_format": "jpeg",
        "base64": True
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200 and "image" in response.json():
        return response.json()["image"]  # Corrected the key name
    else:
        st.error("Failed to generate outfit suggestions. Please try again.")
        return []

# Function to call the FaceSwap API
def apply_faceswap(source_img_base64, target_img_base64, api_key):
    url = "https://api.segmind.com/v1/faceswap-v3"
    data = {
        "source_img": source_img_base64,
        "target_img": target_img_base64,
        "input_faces_index": 0,
        "source_faces_index": 0,
        "face_restore": "codeformer-v0.1.0.pth",
        "interpolation": "Bilinear",
        "detection_face_order": "large-small",
        "facedetection": "retinaface_resnet50",
        "detect_gender_input": "no",
        "detect_gender_source": "no",
        "face_restore_weight": 0.75,
        "image_format": "jpeg",
        "image_quality": 95,
        "base64": True
    }
    headers = {"x-api-key": st.secrets["API"]["api_key"]}
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200 and "image" in response.json():
        return response.json()["image"]
    else:
        st.error("Error applying FaceSwap. Please try again.")
        return None

# Streamlit UI
st.title("Personalized Outfit Suggester")
st.write("Upload your face image and fill in your details to get personalized outfit suggestions.")

# User inputs
body_type = st.selectbox("Body Type", [ "Slim", "Athletic", "Curvy", "Plus Size"])
body_shape = st.selectbox("Body Shape", [ "Rectangle", "Hourglass", "Triangle", "Inverted Triangle", "Pear"])
gender = st.selectbox("Gender", [ "Man", "Woman", "Non-Binary"])
color_complexion = st.selectbox("Color Complexion", [ "Light", "Medium", "Dark","warm wheatish"])
occasion = st.selectbox("occasion", [ "Diwali party", "Wedding", "Christmas Dinner", "Casual day outing", "beach day"])
age = st.selectbox("age", [ "Teens", "Mid-twentys", "Mid-thirtys ", "Mid-fortys", "Mid-fiftys"])
season = st.selectbox("season", [ "summers", "winters", "rainy", "autumn", "spring"])
style = st.selectbox("style", [ "casual", "formal", "bohemian", "vintage", "streetwear", "preppy", "minimalist", "chic","artsy"])
# ethinicity = st.selectbox("ethinicity", [ "Indian", "American", "French", "Spanish"])


uploaded_file = st.file_uploader("Your Face Image", type=["png", "jpg", "jpeg"])

# Button to generate outfits
if st.button("Generate Outfit Suggestions"):
    if uploaded_file and body_type != "Select your body type" and body_shape != "Select your body shape" and gender != "Select your gender" and color_complexion != "Select your color complexion":
        st.info("Processing... This might take a few seconds.")
        
        # Convert uploaded file to base64
        face_image_base64 = image_to_base64(uploaded_file)
        
        # Generate outfit images using Text-to-Image API
        st.info("Generating outfit suggestions...")
        prompt = (
            # f"A full-body image of an Indian {age.lower()} some {gender.lower()} with a {body_shape.lower()} {body_type.lower()} body and {color_complexion.lower()} complexion, for an occasion like {occasion.lower()} "
            f'''A full-body image of an Indian {gender.lower()} in his/her {age.lower()}, dressed for a {occasion.lower()} and in a {style.lower()} style for a {season.lower()} season , 
            with a {color_complexion.lower()} complexion, a {body_type.lower()},and an {body_shape.lower()} shaped body. The outfit is styled to match the occasion, 
            combining elegance, with an emphasis on color tones that complement his/her skin tone. The background subtly reflects the event setting, 
            providing context but ensuring the focus is entirely on the outfit. The outfit includes intricate details, appropriate footwear, and accessories, styled cohesively 
            for a polished look. Lighting is natural and soft, enhancing the colors and textures of the clothing and accessories.'''
            # f"wearing fashionable, full-body outfits. Detailed face, proportional body, head included, realistic images, the background should be in accordance with the occasion"
        )
        generated_images = generate_outfits(prompt, st.secrets["API"]["api_key"])

        
        if generated_images:
            st.info("Applying FaceSwap to the generated outfits...")
            swapped_images = []
            
            for img_base64 in generated_images:
                swapped_image = apply_faceswap(face_image_base64, img_base64, st.secrets["API"]["api_key"])
                if swapped_image:
                    swapped_images.append(swapped_image)
            
            if swapped_images:
                st.subheader("Suggested Outfits:")
                col1, col2 = st.columns(2)
                col3, col4 = st.columns(2)
                columns = [col1, col2, col3, col4]
                
                # Display swapped images in 2x2 layout
                for i, img_base64 in enumerate(swapped_images):
                    with columns[i]:
                        image = decode_base64_to_image(img_base64)
                        st.image(image, use_container_width=True)
        else:
            st.error("Failed to generate outfit suggestions.")
    else:
        st.error("Please fill in all the details and upload your face image.")
