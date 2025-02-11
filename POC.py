import streamlit as st
import requests
import base64
import concurrent.futures
from PIL import Image
from io import BytesIO
import random
from datetime import datetime
import json

# ----- Helper Functions -----
def image_to_base64(image):
    """Resize the uploaded image and convert it to Base64."""
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

def generate_outfits(prompt, face_image_base64):
    """Call the Text-to-Image API (Stable Diffusion) to generate an outfit image."""
    url = "https://api.segmind.com/v1/stable-diffusion-3.5-large-txt2img"
    headers = {"x-api-key": st.secrets["API"]["api_key"]}
    data = {
        "prompt": prompt,
        "negative_prompt": (
            "Blurry details, incomplete outfit, disproportionate body shape, overly bright or unnatural lighting, unrealistic or overly exaggerated features, "
            "distracting backgrounds, mismatched accessories, poorly styled or irrelevant attire, inconsistent textures, low-quality rendering and multiple images, "
            "same clothes in all the images, (same colour), multiple body parts"
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
        now = datetime.now()
        print("now = generated", now)
        if response.status_code == 200 and "image" in response_json:
            return apply_faceswap(face_image_base64, response_json("image"))
            # return response_json["image"]
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
        now = datetime.now()
        print("now =", now)
        if response.status_code == 200 and "image" in response_json:
            return response_json["image"]
        else:
            st.error(f"Error applying FaceSwap: {response_json.get('error', 'Unknown error')}")
        return None
    except Exception as e:
        st.error(f"Unexpected error during FaceSwap: {str(e)}")
        return None

# ----- Custom CSS for Background, Header, Button, and Progress Bar Labels -----
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1638361634616-10ae6b8d8af4?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
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
        margin-right: 0px;
        margin-left: 0px;  /* Added left margin for better alignment with select boxes */ 
    }
    
    .progress-labels {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
        font-weight: bold;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom progress bar labels above the progress bar

st.markdown(
    """
    <div class="progress-labels">
        <span>1. Intro</span>
        <span>2. Body</span>
        <span>3. Theme</span>
        <span>4. Preview</span>
        <span>5. Outfits</span>
    </div>
    """,
    unsafe_allow_html=True
)

# ----- Multi-page Navigation Setup -----
if "page" not in st.session_state:
    st.session_state["page"] = "intro"
if "progress" not in st.session_state:
    st.session_state["progress"] = 0
if "generated_images" not in st.session_state:
    st.session_state["generated_images"] = None

def go_to_page(page_name, progress, reset_generated=False):
    st.session_state["page"] = page_name
    st.session_state["progress"] = progress
    if reset_generated:
        st.session_state["generated_images"] = None
    # st.session_state["force_update"] = not st.session_state.get("force_update", False)
    st.rerun()


# Display progress bar at the top
st.progress(st.session_state["progress"])

# ----- Page Definitions -----

# Intro Page
if st.session_state["page"] == "intro":
    st.title("Welcome to Personalized Outfit Suggester!")
    st.write("Discover outfit suggestions tailored to your style and body type with a fun face-swap twist!")
    if st.button("Start Now", key="start_intro"):
        go_to_page("body_details", 20)

# Page 1: Body Details
elif st.session_state["page"] == "body_details":
    st.title("Step 1: Tell us about your body")
    body_type = st.selectbox("Body Type", ["Slim", "Athletic", "Curvy", "Plus Size"], key="body_type_input",
                              index=["Slim", "Athletic", "Curvy", "Plus Size"].index(st.session_state.get("body_type", "Slim")))
    body_shape = st.selectbox("Body Shape", ["Rectangle", "Hourglass", "Triangle", "Inverted Triangle", "Pear"], key="body_shape_input",
                               index=["Rectangle", "Hourglass", "Triangle", "Inverted Triangle", "Pear"].index(st.session_state.get("body_shape", "Rectangle")))
    gender = st.selectbox("Gender", ["Man", "Woman", "Non-Binary"], key="gender_input",
                          index=["Man", "Woman", "Non-Binary"].index(st.session_state.get("gender", "Man")))
    age = st.selectbox("Age", ["15 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65 - 75"], key="age_input",
                       index=["15 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65 - 75"].index(st.session_state.get("age", "15 - 24")))
    color_complexion = st.selectbox("Color Complexion", ["Light", "Medium", "Dark", "warm wheatish"], key="complexion_input",
                                    index=["Light", "Medium", "Dark", "warm wheatish"].index(st.session_state.get("color_complexion", "Light")))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Intro", key="back_intro"):
            go_to_page("intro", 0)
    with col2:
        if st.button("Next", key="next_body"):
            st.session_state["body_type"] = body_type
            st.session_state["body_shape"] = body_shape
            st.session_state["gender"] = gender
            st.session_state["age"] = age
            st.session_state["color_complexion"] = color_complexion
            go_to_page("preferences", 40)

# Page 2: Fashion Preferences & Face Image Upload
elif st.session_state["page"] == "preferences":
    st.title("Step 2: Your Theme Preferences")
    occasion = st.selectbox("Occasion", ["Diwali party", "Wedding", "Christmas Dinner", "Casual day outing", "beach day"], key="occasion_input",
                             index=["Diwali party", "Wedding", "Christmas Dinner", "Casual day outing", "beach day"].index(st.session_state.get("occasion", "Diwali party")))
    season = st.selectbox("Season", ["summers", "winters", "rainy", "autumn", "spring"], key="season_input",
                          index=["summers", "winters", "rainy", "autumn", "spring"].index(st.session_state.get("season", "summers")))
    style = st.selectbox("Style", ["casual", "formal", "bohemian", "vintage", "streetwear", "preppy", "minimalist", "chic", "artsy"], key="style_input",
                         index=["casual", "formal", "bohemian", "vintage", "streetwear", "preppy", "minimalist", "chic", "artsy"].index(st.session_state.get("style", "casual")))
    ethinicity = st.selectbox("Ethinicity", ["Indian", "American", "French", "Spanish"], key="ethinicity_input",
                              index=["Indian", "American", "French", "Spanish"].index(st.session_state.get("ethinicity", "Indian")))
    st.subheader("Upload Your Face Image")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="face_upload")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", key="back_preferences"):
            go_to_page("body_details", 20)
    with col2:
        if st.button("Next to Preview", key="next_preview"):
            st.session_state["occasion"] = occasion
            st.session_state["season"] = season
            st.session_state["style"] = style
            st.session_state["ethinicity"] = ethinicity
            st.session_state["uploaded_file"] = uploaded_file
            go_to_page("preview", 60)

# Page 3: Preview User Choices
elif st.session_state["page"] == "preview":
    st.title("Preview Your Choices")
    st.write("Review your selections below before generating outfit suggestions:")
    st.write("**Body Details:**")
    st.write(f"Body Type: {st.session_state.get('body_type', 'Not set')}")
    st.write(f"Body Shape: {st.session_state.get('body_shape', 'Not set')}")
    st.write(f"Gender: {st.session_state.get('gender', 'Not set')}")
    st.write(f"Age: {st.session_state.get('age', 'Not set')}")
    st.write(f"Color Complexion: {st.session_state.get('color_complexion', 'Not set')}")
    st.write("**Theme Preferences:**")
    st.write(f"Occasion: {st.session_state.get('occasion', 'Not set')}")
    st.write(f"Season: {st.session_state.get('season', 'Not set')}")
    st.write(f"Style: {st.session_state.get('style', 'Not set')}")
    st.write(f"Ethinicity: {st.session_state.get('ethinicity', 'Not set')}")
    if st.session_state.get("uploaded_file") is not None:
        st.image(decode_base64_to_image(image_to_base64(st.session_state.get("uploaded_file"))), width=200)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Preferences", key="back_to_preferences"):
            go_to_page("preferences", 40)
    # Removed "Update Preview" button per your request
    with col2:
        if st.button("Confirm and Generate", key="confirm_generate"):
            go_to_page("results", 100)

# Page 4: Results Page
elif st.session_state["page"] == "results":
    st.title("Your Personalized Outfit Suggestions")
    
    # Retrieve saved inputs
    body_type = st.session_state.get("body_type")
    body_shape = st.session_state.get("body_shape")
    gender = st.session_state.get("gender")
    age = st.session_state.get("age")
    color_complexion = st.session_state.get("color_complexion")
    occasion = st.session_state.get("occasion")
    season = st.session_state.get("season")
    style = st.session_state.get("style")
    ethinicity = st.session_state.get("ethinicity")
    uploaded_file = st.session_state.get("uploaded_file")
    
    if not uploaded_file:
        st.error("No face image uploaded. Please go back and upload your face image.")
    else:
        face_image_base64 = image_to_base64(uploaded_file)
        if not face_image_base64:
            st.error("Failed to process the face image.")
        else:
            st.info("Generating outfit suggestions...")
            # Generate unique variations for outfit details
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
                f"The background shouldn't be blurry and faded."
                for i in range(4)
            ]

            # --- Multithreading: Generate outfit images concurrently ---
            with concurrent.futures.ThreadPoolExecutor() as executor:
                print("thread execution start")
                now = datetime.now()
                print("now =", now)
                futures = [executor.submit(generate_outfits, prompt, face_image_base64) for prompt in prompts]
                print("thread execution complete")
                now = datetime.now()
                print("now =", now)
                # Retrieve results in order of submission
                generated_images = [f.result() for f in futures if f.result() is not None]
            
            # if generated_images:
            #     now = datetime.now()
            #     print("now = kkk", now)
            #     st.info("Applying FaceSwap to the generated outfits...")
            #     # --- Multithreading: Apply FaceSwap concurrently ---
            #     with concurrent.futures.ThreadPoolExecutor() as executor:
            #         swapped_images = list(executor.map(lambda img: apply_faceswap(face_image_base64, img), generated_images))
            #     # Filter out any None results from FaceSwap
                generated_images = [img for img in generated_images if img is not None]
                
            if generated_images:
                st.subheader("Suggested Outfits:")
                cols = st.columns(2)
                for i, img_base64 in enumerate(generated_images):
                    with cols[i % 2]:
                        image = decode_base64_to_image(img_base64)
                        if image:
                            st.image(image, use_container_width=True)
            else:
                st.error("FaceSwap failed for all images.")
            # else:
            #     st.error("Failed to generate outfit suggestions.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Edit Inputs", key="edit_inputs"):
            go_to_page("preview", 80)
    with col2:
        if st.button("Start Over", key="start_over"):
            st.session_state.clear()
            go_to_page("intro", 0, reset_generated=True)
            
    #         # Generate outfit images for each prompt separately
    #         generated_images = []
    #         for single_prompt in prompts:
    #             img_base64 = generate_outfits(single_prompt)
    #             if img_base64:
    #                 generated_images.append(img_base64)
            
    #         if generated_images:
    #             st.info("Applying FaceSwap to the generated outfits...")
    #             swapped_images = []
    #             for img_base64 in generated_images:
    #                 swapped_image = apply_faceswap(face_image_base64, img_base64)
    #                 if swapped_image:
    #                     swapped_images.append(swapped_image)
                
    #             if swapped_images:
    #                 st.subheader("Suggested Outfits:")
    #                 cols = st.columns(2)
    #                 for i, img_base64 in enumerate(swapped_images):
    #                     with cols[i % 2]:
    #                         image = decode_base64_to_image(img_base64)
    #                         if image:
    #                             st.image(image, use_container_width=True)
    #             else:
    #                 st.error("FaceSwap failed for all images.")
    #         else:
    #             st.error("Failed to generate outfit suggestions.")
    
    # col1, col2 = st.columns(2)
    # with col1:
    #     if st.button("Edit Inputs", key="edit_inputs"):
    #         go_to_page("preview", 80)
    # with col2:
    #     if st.button("Start Over", key="start_over"):
    #         st.session_state.clear()
    #         go_to_page("intro", 0, reset_generated=True)
