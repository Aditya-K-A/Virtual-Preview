import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import random

# Helper function: Convert image to Base64
def image_to_base64(image):
    try:
        img = Image.open(image)
        img = img.resize((512, 512))  # Resize to prevent API errors
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        st.error(f"Error converting image to Base64: {str(e)}")
        return None

# Helper function: Decode Base64 to Image
def decode_base64_to_image(base64_data):
    try:
        return Image.open(BytesIO(base64.b64decode(base64_data)))
    except Exception as e:
        st.error(f"Error decoding Base64 image: {str(e)}")
        return None

# Function to call the Text-to-Image API
def generate_outfits(prompt):
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
        "batch_size": 1,  # Generate one image per prompt
        "image_format": "jpeg",
        "base64": True
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()
        if response.status_code == 200 and "image" in response_json:
            return response_json["image"]
        else:
            st.error(f"Failed to generate outfit suggestions. {response_json.get('error', '')}")
            return None
    except Exception as e:
        st.error(f"Unexpected error in Text-to-Image API: {str(e)}")
        return None

# Function to call the FaceSwap API
def apply_faceswap(source_img_base64, target_img_base64):
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

# Streamlit UI
st.title("Personalized Outfit Suggester")
st.write("Upload your face image and fill in your details to get personalized outfit suggestions.")

# --- User Inputs (9 fields) ---
body_type = st.selectbox("Body Type", ["Slim", "Athletic", "Curvy", "Plus Size"])
body_shape = st.selectbox("Body Shape", ["Rectangle", "Hourglass", "Triangle", "Inverted Triangle", "Pear"])
gender = st.selectbox("Gender", ["Man", "Woman", "Non-Binary"])
color_complexion = st.selectbox("Color Complexion", ["Light", "Medium", "Dark", "warm wheatish"])
occasion = st.selectbox("Occasion", ["Diwali party", "Wedding", "Christmas Dinner", "Casual day outing", "beach day"])
age = st.selectbox("Age", ["Teens", "Mid-twentys", "Mid-thirtys", "Mid-fortys", "Mid-fiftys"])
season = st.selectbox("Season", ["summers", "winters", "rainy", "autumn", "spring"])
style = st.selectbox("Style", ["casual", "formal", "bohemian", "vintage", "streetwear", "preppy", "minimalist", "chic", "artsy"])
ethinicity = st.selectbox("Ethinicity", ["Indian", "American", "French", "Spanish"])

# --- Additional parameters for outfit variations ---
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

uploaded_file = st.file_uploader("Your Face Image", type=["png", "jpg", "jpeg"])

if st.button("Generate Outfit Suggestions"):
    if uploaded_file:
        st.info("Processing... This might take a few seconds.")
        face_image_base64 = image_to_base64(uploaded_file)
        if not face_image_base64:
            st.error("Failed to process the face image.")
        else:
            st.info("Generating outfit suggestions...")
            # Modified the prompt to ensure that the full head and face are clearly visible.
            prompts = [
                (
                    f"A full-body image of an {ethinicity.lower()} {gender.lower()} in their {age.lower()} dressed for a {occasion.lower()} for the {season.lower()} season, with a clearly visible head and face. "
                    f"The outfit should be {selected_clothing_variations[i]} in accordance with {style.lower()} style in {selected_colors[i]} color with a {selected_patterns[i]} pattern. "
                    f"The background should be {selected_backgrounds[i]}. "
                    "Ensure no two images have the same color scheme, fabric, or clothing type. "
                    "The attire should include appropriate footwear and accessories to complete the look. "
                    "Do not include multiple people in a single image. There should only be one person in an image at a time. "
                    "Lighting should be natural and soft, enhancing the colors and textures of the clothing and accessories."
                )
                for i in range(4)
            ]
            
            generated_images = []
            for single_prompt in prompts:
                image = generate_outfits(single_prompt)
                if image:
                    generated_images.append(image)

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
    else:
        st.error("Please fill in all the details and upload your face image.")
