# import streamlit as st
# import requests
# import base64
# from PIL import Image
# from io import BytesIO

# # Helper functions for image handling
# def image_to_base64(image):
#     return base64.b64encode(image.read()).decode("utf-8")

# def decode_base64_to_image(base64_data):
#     return Image.open(BytesIO(base64.b64decode(base64_data)))

# # Function to call the Text-to-Image API
# def generate_outfits(prompt, api_key):
#     url = "https://api.segmind.com/v1/stable-diffusion-3.5-large-txt2img"
#     headers = {"x-api-key": st.secrets["API"]["api_key"]}
#     data = {
#         "prompt": prompt,
#         # "negative_prompt": "low quality, blurry, cropped head, disfigured face, animated",
#         "negative_prompt": '''Blurry details, incomplete outfit, disproportionate body shape, overly bright or unnatural lighting, unrealistic or overly exaggerated features, 
#          distracting backgrounds, mismatched accessories, poorly styled or irrelevant attire, inconsistent textures, or low-quality rendering''',
#         "steps": 50,  # Increased for better quality
#         "guidance_scale": 7.5,  # Increased to emphasize prompt details
#         "seed": 98552302,
#         "sampler": "euler",
#         "scheduler": "sgm_uniform",
#         "width": 768,  # Adjusted dimensions for better proportions
#         "height": 1024,  # Ensures full-body images with heads
#         "batch_size": 4,
#         "image_format": "jpeg",
#         "base64": True
#     }

#     response = requests.post(url, json=data, headers=headers)

#     if response.status_code == 200 and "image" in response.json():
#         return response.json()["image"]  # Corrected the key name
#     else:
#         st.error("Failed to generate outfit suggestions. Please try again.")
#         return []

# # Function to call the FaceSwap API
# def apply_faceswap(source_img_base64, target_img_base64, api_key):
#     url = "https://api.segmind.com/v1/faceswap-v3"
#     data = {
#         "source_img": source_img_base64,
#         "target_img": target_img_base64,
#         "input_faces_index": 0,
#         "source_faces_index": 0,
#         "face_restore": "codeformer-v0.1.0.pth",
#         "interpolation": "Bilinear",
#         "detection_face_order": "large-small",
#         "facedetection": "retinaface_resnet50",
#         "detect_gender_input": "no",
#         "detect_gender_source": "no",
#         "face_restore_weight": 0.75,
#         "image_format": "jpeg",
#         "image_quality": 95,
#         "base64": True
#     }
#     headers = {"x-api-key": st.secrets["API"]["api_key"]}
#     response = requests.post(url, json=data, headers=headers)
    
#     if response.status_code == 200 and "image" in response.json():
#         return response.json()["image"]
#     else:
#         st.error("Error applying FaceSwap. Please try again.")
#         return None

# # Streamlit UI
# st.title("Personalized Outfit Suggester")
# st.write("Upload your face image and fill in your details to get personalized outfit suggestions.")

# # User inputs
# body_type = st.selectbox("Body Type", [ "Slim", "Athletic", "Curvy", "Plus Size"])
# body_shape = st.selectbox("Body Shape", [ "Rectangle", "Hourglass", "Triangle", "Inverted Triangle", "Pear"])
# gender = st.selectbox("Gender", [ "Man", "Woman", "Non-Binary"])
# color_complexion = st.selectbox("Color Complexion", [ "Light", "Medium", "Dark","warm wheatish"])
# occasion = st.selectbox("occasion", [ "Diwali party", "Wedding", "Christmas Dinner", "Casual day outing", "beach day"])
# age = st.selectbox("age", [ "Teens", "Mid-twentys", "Mid-thirtys ", "Mid-fortys", "Mid-fiftys"])
# season = st.selectbox("season", [ "summers", "winters", "rainy", "autumn", "spring"])
# style = st.selectbox("style", [ "casual", "formal", "bohemian", "vintage", "streetwear", "preppy", "minimalist", "chic","artsy"])
# # ethinicity = st.selectbox("ethinicity", [ "Indian", "American", "French", "Spanish"])


# uploaded_file = st.file_uploader("Your Face Image", type=["png", "jpg", "jpeg"])

# # Button to generate outfits
# if st.button("Generate Outfit Suggestions"):
#     if uploaded_file and body_type != "Select your body type" and body_shape != "Select your body shape" and gender != "Select your gender" and color_complexion != "Select your color complexion":
#         st.info("Processing... This might take a few seconds.")
        
#         # Convert uploaded file to base64
#         face_image_base64 = image_to_base64(uploaded_file)
        
#         # Generate outfit images using Text-to-Image API
#         st.info("Generating outfit suggestions...")
#         prompt = (
#             # f"A full-body image of an Indian {age.lower()} some {gender.lower()} with a {body_shape.lower()} {body_type.lower()} body and {color_complexion.lower()} complexion, for an occasion like {occasion.lower()} "
#             f'''A full-body image of an Indian {gender.lower()} in his/her {age.lower()}, dressed for a {occasion.lower()} and in a {style.lower()} style for a {season.lower()} season , 
#             with a {color_complexion.lower()} complexion, a {body_type.lower()},and an {body_shape.lower()} shaped body. The outfit is styled to match the occasion, 
#             combining elegance, with an emphasis on color tones that complement his/her skin tone. The background subtly reflects the event setting, 
#             providing context but ensuring the focus is entirely on the outfit. The outfit includes intricate details, appropriate footwear, and accessories, styled cohesively 
#             for a polished look. Lighting is natural and soft, enhancing the colors and textures of the clothing and accessories.'''
#             # f"wearing fashionable, full-body outfits. Detailed face, proportional body, head included, realistic images, the background should be in accordance with the occasion"
#         )
#         generated_images = generate_outfits(prompt, st.secrets["API"]["api_key"])

        
#         if generated_images:
#             st.info("Applying FaceSwap to the generated outfits...")
#             swapped_images = []
            
#             for img_base64 in generated_images:
#                 swapped_image = apply_faceswap(face_image_base64, img_base64, st.secrets["API"]["api_key"])
#                 if swapped_image:
#                     swapped_images.append(swapped_image)
            
#             if swapped_images:
#                 st.subheader("Suggested Outfits:")
#                 col1, col2 = st.columns(2)
#                 col3, col4 = st.columns(2)
#                 columns = [col1, col2, col3, col4]
                
#                 # Display swapped images in 2x2 layout
#                 for i, img_base64 in enumerate(swapped_images):
#                     with columns[i]:
#                         image = decode_base64_to_image(img_base64)
#                         st.image(image, use_container_width=True)
#         else:
#             st.error("Failed to generate outfit suggestions.")
#     else:
#         st.error("Please fill in all the details and upload your face image.")



import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import random
import json

# ----- Helper Functions -----
def image_to_base64(image):
    """Convert an uploaded image to Base64 after resizing it."""
    try:
        img = Image.open(image)
        img = img.resize((512, 512))  # Resize for API compatibility
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        st.error(f"Error converting image to Base64: {str(e)}")
        return None

def decode_base64_to_image(b64_data):
    """Decode a Base64 string back to an Image."""
    try:
        return Image.open(BytesIO(base64.b64decode(b64_data)))
    except Exception as e:
        st.error(f"Error decoding Base64 image: {str(e)}")
        return None

def generate_outfits(prompt):
    """Call the Text-to-Image API (Stable Diffusion) to generate an outfit image."""
    url = "https://api.segmind.com/v1/stable-diffusion-3.5-large-txt2img"
    headers = {"x-api-key": st.secrets["API"]["api_key"]}
    data = {
        "prompt": prompt,
        "negative_prompt": (
            "Blurry details, incomplete outfit, disproportionate body shape, overly bright or unnatural lighting, "
            "unrealistic or overly exaggerated features, distracting backgrounds, mismatched accessories, poorly styled "
            "or irrelevant attire, inconsistent textures, low-quality rendering and multiple images, same clothes in all "
            "the images, (same colour), multiple body parts"
        ),
        "steps": 35,
        "guidance_scale": 7.5,
        "seed": random.randint(1, 99999999),
        "sampler": "euler_a",
        "scheduler": "sgm_uniform",
        "width": 768,
        "height": 1024,
        "batch_size": 1,  # One image per prompt
        "image_format": "jpeg",
        "base64": True
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()
        if response.status_code == 200 and "image" in response_json:
            return response_json["image"]
        else:
            st.error(f"Failed to generate outfit suggestions. {response_json.get('error', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Unexpected error in Text-to-Image API: {str(e)}")
        return None

def apply_faceswap(source_img_base64, target_img_base64):
    """Call the FaceSwap API to swap the user's face onto the generated outfit image."""
    if not target_img_base64 or len(target_img_base64) < 100:
        st.error("Invalid target image. Skipping FaceSwap.")
        return None

    url = "https://api.segmind.com/v1/faceswap-v3"
    data = {
        "source_img": source_img_base64,
        "target_img": target_img_base64,
        "input_faces_index": 0,
        "source_faces_index": 0,
        "face_restore": "codeformer-v0.1.0.pth",
        "interpolation": "Bicubic",
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
    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()
        if response.status_code == 200 and "image" in response_json:
            return response_json["image"]
        else:
            st.error(f"Error applying FaceSwap: {response_json.get('error', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Unexpected error during FaceSwap: {str(e)}")
        return None

# ----- Custom CSS for Background and Button Styling -----
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://i.pinimg.com/736x/59/97/80/5997806b417a45fdf9e6a7dbd54dc8f0.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .stButton>button {
        border-radius: 10px;
        padding: 10px 20px;
        background-color: #ff6f61;
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----- Multi-page Navigation Using Session State -----
if "page" not in st.session_state:
    st.session_state["page"] = "intro"
if "progress" not in st.session_state:
    st.session_state["progress"] = 0

def go_to_page(page_name, progress):
    st.session_state["page"] = page_name
    st.session_state["progress"] = progress

# Progress bar at the top
st.progress(st.session_state["progress"])

# ----- Page Definitions -----

# Intro Page
if st.session_state["page"] == "intro":
    st.title("Welcome to Personalized Outfit Suggester!")
    st.write("This app helps you discover outfit suggestions tailored to your style and body type with a fun face-swap twist!")
    if st.button("Start"):
        go_to_page("body_details", 33)

# Page 1: Body Details
elif st.session_state["page"] == "body_details":
    st.title("Step 1: Tell us about your body")
    body_type = st.selectbox("Body Type", ["Slim", "Athletic", "Curvy", "Plus Size"])
    body_shape = st.selectbox("Body Shape", ["Rectangle", "Hourglass", "Triangle", "Inverted Triangle", "Pear"])
    gender = st.selectbox("Gender", ["Man", "Woman", "Non-Binary"])
    color_complexion = st.selectbox("Color Complexion", ["Light", "Medium", "Dark", "warm wheatish"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Intro"):
            go_to_page("intro", 0)
    with col2:
        if st.button("Next"):
            # Save body details into session state
            st.session_state["body_type"] = body_type
            st.session_state["body_shape"] = body_shape
            st.session_state["gender"] = gender
            st.session_state["color_complexion"] = color_complexion
            go_to_page("preferences", 66)

# Page 2: Fashion Preferences & Face Image Upload
elif st.session_state["page"] == "preferences":
    st.title("Step 2: Your Fashion Preferences")
    occasion = st.selectbox("Occasion", ["Diwali party", "Wedding", "Christmas Dinner", "Casual day outing", "beach day"])
    age = st.selectbox("Age", ["Teens", "Mid-twentys", "Mid-thirtys", "Mid-fortys", "Mid-fiftys"])
    season = st.selectbox("Season", ["summers", "winters", "rainy", "autumn", "spring"])
    style = st.selectbox("Style", ["casual", "formal", "bohemian", "vintage", "streetwear", "preppy", "minimalist", "chic", "artsy"])
    ethinicity = st.selectbox("Ethinicity", ["Indian", "American", "French", "Spanish"])
    st.subheader("Upload Your Face Image")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            go_to_page("body_details", 33)
    with col2:
        if st.button("Generate Outfit Suggestions"):
            # Save fashion preferences into session state
            st.session_state["occasion"] = occasion
            st.session_state["age"] = age
            st.session_state["season"] = season
            st.session_state["style"] = style
            st.session_state["ethinicity"] = ethinicity
            st.session_state["uploaded_file"] = uploaded_file
            go_to_page("results", 100)

# Results Page
elif st.session_state["page"] == "results":
    st.title("Your Personalized Outfit Suggestions")
    
    # Retrieve saved inputs
    body_type = st.session_state.get("body_type")
    body_shape = st.session_state.get("body_shape")
    gender = st.session_state.get("gender")
    color_complexion = st.session_state.get("color_complexion")
    occasion = st.session_state.get("occasion")
    age = st.session_state.get("age")
    season = st.session_state.get("season")
    style = st.session_state.get("style")
    ethinicity = st.session_state.get("ethinicity")
    uploaded_file = st.session_state.get("uploaded_file")
    
    # Check if face image is uploaded
    if not uploaded_file:
        st.error("No face image uploaded. Please go back and upload your face image.")
    else:
        face_image_base64 = image_to_base64(uploaded_file)
        if not face_image_base64:
            st.error("Failed to process the face image.")
        else:
            st.info("Generating outfit suggestions...")
            # For extra outfit variety, generate unique variations for clothing, colors, patterns, backgrounds:
            color_variations = [
                "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown",
                "black", "cyan", "magenta", "lime", "teal", "maroon", "navy", "olive"
            ]
            patterns = ["striped", "solid", "polka dots", "floral", "plain"]
            background_variations = ["natural outdoor setting", "minimalist indoor space", "festive backdrop", "modern studio setup"]
            clothing_variations = [
                "A well-tailored or structured outfit, such as a suit, blazer with trousers, or a chic co-ord set.",
                "A relaxed and effortless ensemble, like a flowy dress, oversized top with fitted bottoms, or a tunic with wide-leg pants.",
                "A statement piece that defines the look, such as a bold-printed jacket, an asymmetrical top, or a textured layer like a poncho or cape.",
                "A mix of classic and trendy elements, like high-waisted pants with a cropped top, a stylish midi skirt, or a fusion-inspired outfit with modern cuts."
            ]
            selected_clothing_variations = random.sample(clothing_variations, 4)
            selected_colors = random.sample(color_variations, 4)
            selected_patterns = random.sample(patterns, 4)
            selected_backgrounds = random.sample(background_variations, 4)
            
            # Generate 4 unique prompts using the selected variations
            prompts = [
                f"A full-body image of an {ethinicity.lower()} {gender.lower()} in their {age.lower()}, with a {color_complexion.lower()} and a {body_type.lower()} {body_shape.lower()} shaped body, dressed for a {occasion.lower()} for the {season.lower()} season. "
                f"The outfit should be {selected_clothing_variations[i]} in accordance with {style.lower()} style in {selected_colors[i]} color with a {selected_patterns[i]} pattern. "
                f"The background should be {selected_backgrounds[i]}. "
                f"Ensure no two images have the same color scheme, fabric, or clothing type. "
                f"The attire should include appropriate footwear and accessories to complete the look. "
                f"Do not include multiple people in a single image. There should only be one person in an image at a time. "
                f"Lighting should be natural and soft, enhancing the colors and textures of the clothing and accessories."
                for i in range(4)
            ]
            
            # Generate outfit images for each prompt separately
            generated_images = []
            for single_prompt in prompts:
                img_base64 = generate_outfits(single_prompt)
                if img_base64:
                    generated_images.append(img_base64)
            
            if generated_images:
                st.info("Applying FaceSwap to the generated outfits...")
                swapped_images = []
                for img_base64 in generated_images:
                    swapped_image = apply_faceswap(face_image_base64, img_base64)
                    if swapped_image:
                        swapped_images.append(swapped_image)
                
                if swapped_images:
                    st.subheader("Suggested Outfits:")
                    cols = st.columns(2)
                    for i, img_base64 in enumerate(swapped_images):
                        with cols[i % 2]:
                            image = decode_base64_to_image(img_base64)
                            if image:
                                st.image(image, use_container_width=True)
                else:
                    st.error("FaceSwap failed for all images.")
            else:
                st.error("Failed to generate outfit suggestions.")
    
    if st.button("Start Over"):
        go_to_page("intro", 0)
