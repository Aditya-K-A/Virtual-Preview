# import streamlit as st
# from PIL import Image

# st.title("Personalized Outfit Suggester")

# with st.form("user_inputs_form"):
#     st.subheader("Enter Your Details:")

#     body_type = st.selectbox("Body Type", ["Slim", "Athletic", "Curvy", "Broad"])
#     body_shape = st.selectbox("Body Shape", ["Rectangle", "Hourglass", "Oval", "Inverted Triangle"])
#     gender = st.selectbox("Gender", ["Male", "Female", "Other"])
#     color_complexion = st.selectbox("Color Complexion", ["Fair", "Medium", "Dark", "Olive"])
#     # occasion = pass
#     # dayt time = 

    
#     uploaded_image = st.file_uploader("Your Face Image", type=["png", "jpg", "jpeg"])

#     submitted = st.form_submit_button("Generate Outfit Suggestions")

# if submitted:
#     if uploaded_image is None:
#         st.error("Please upload a face image!")
#     else:
#         st.subheader("Uploaded Face Image:")
#         face_image = Image.open(uploaded_image)
#         st.image(face_image, caption="Your Face Image", use_container_width=True)

#         st.subheader("Suggested Outfits:")

#         cols = st.columns(4)  
#         for col in cols:
#             with col:
#                 st.image("https://i.pinimg.com/736x/00/db/dc/00dbdcaf451ebfeb0e10a917b482952e.jpg", use_container_width=True, caption="Outfit Suggestion")


# import streamlit as st

# st.set_page_config(
#     page_title="Personalized Outfit Suggester",
#     layout="wide",  # Enable wide layout
#     initial_sidebar_state="expanded",
# )

# st.title("Personalized Outfit Suggester")
# st.write("Upload your face image and get personalized outfit suggestions based on your preferences!")

# st.subheader("Enter Your Details:")

# with st.form("user_input_form"):
#     body_type = st.selectbox("Body Type", ["Slim", "Athletic", "Average", "Curvy"])
#     body_shape = st.selectbox("Body Shape", ["Rectangle", "Hourglass", "Pear","Inverted Triangle"])
#     gender = st.selectbox("Gender", ["Male", "Female", "Other"])
#     complexion = st.selectbox("Color Complexion", ["Fair", "Medium", "Tan", "Dark"])
#     uploaded_file = st.file_uploader("Your Face Image", type=["png", "jpg", "jpeg"])
    
#     submitted = st.form_submit_button("Generate Outfit Suggestions")

# if submitted:
#     if not uploaded_file:
#         st.error("Please upload a valid face image.")
#     else:
#         if uploaded_file.size > 2 * 1024 * 1024:  
#             st.error("File size exceeds 2 MB. Please upload a smaller file.")
#         else:
#             st.subheader("Uploaded Face Image:")
#             st.image(uploaded_file, caption="Your Image", use_container_width=True)
#             st.subheader("Suggested Outfits:")
#             cols = st.columns(5)  
#             for i, col in enumerate(cols):
#                 with col:
#                     st.image("https://via.placeholder.com/150", caption=f"Outfit Suggestion {i+1}", use_container_width=True)





# import streamlit as st
# import requests
# import base64
# from PIL import Image
# from io import BytesIO

# # Helper functions for image handling
# def image_file_to_base64(image_path):
#     with open(image_path, "rb") as f:
#         image_data = f.read()
#     return base64.b64encode(image_data).decode("utf-8")

# def image_to_base64(image):
#     return base64.b64encode(image.read()).decode("utf-8")

# def decode_base64_to_image(base64_data):
#     return Image.open(BytesIO(base64.b64decode(base64_data)))

# # Function to call the Text-to-Image API
# def generate_outfits(prompt, api_key):
#     url = "https://api.segmind.com/v1/stable-diffusion-3.5-large-txt2img"
#     data = {
#         "prompt": prompt,
#         "negative_prompt": "low quality, blurry",
#         "steps": 25,
#         "guidance_scale": 5.5,
#         "seed": 98552302,
#         "sampler": "euler",
#         "scheduler": "sgm_uniform",
#         "width": 1024,
#         "height": 1024,
#         "aspect_ratio": "custom",
#         "batch_size": 4,  # Generate 4 images
#         "image_format": "jpeg",
#         "image_quality": 95,
#         "base64": True
#     }
#     headers = {"x-api-key": "SG_b10384629aa194e1"}
#     response = requests.post(url, json=data, headers=headers)
    
#     if response.status_code == 200:
#         return response.json()["images"]  # List of base64 images
#     else:
#         st.error("Error generating outfits. Please try again.")
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
#     headers = {"x-api-key": "SG_b10384629aa194e1"}
#     response = requests.post(url, json=data, headers=headers)
    
#     if response.status_code == 200:
#         return response.json()["image"]
#     else:
#         st.error("Error applying FaceSwap. Please try again.")
#         return None

# # Streamlit UI
# st.title("Personalized Outfit Suggester")
# st.write("Upload your face image and fill in your details to get personalized outfit suggestions.")

# # User inputs
# body_type = st.selectbox("Body Type", ["Slim", "Athletic", "Curvy", "Plus Size"])
# body_shape = st.selectbox("Body Shape", ["Rectangle", "Hourglass", "Triangle", "Inverted Triangle"])
# gender = st.selectbox("Gender", ["Male", "Female", "Non-Binary"])
# color_complexion = st.selectbox("Color Complexion", ["Light", "Medium", "Dark"])
# uploaded_file = st.file_uploader("Your Face Image", type=["png", "jpg", "jpeg"])

# # Button to generate outfits
# if st.button("Generate Outfit Suggestions"):
#     if uploaded_file and body_type != "Select your body type" and body_shape != "Select your body shape" and gender != "Select your gender" and color_complexion != "Select your color complexion":
#         st.info("Processing... This might take a few seconds.")
        
#         # Convert uploaded file to base64
#         face_image_base64 = image_to_base64(uploaded_file)
        
#         # Generate outfit images using Text-to-Image API
#         st.info("Generating outfit suggestions...")
#         text_to_image_api_key = "YOUR_TEXT_TO_IMAGE_API_KEY"
#         prompt = f"A {gender.lower()} with a {body_type.lower()} body and {color_complexion.lower()} complexion wearing stylish outfits."
#         generated_images = generate_outfits(prompt, text_to_image_api_key)
        
#         if generated_images:
#             st.info("Applying FaceSwap to the generated outfits...")
#             faceswap_api_key = "YOUR_FACESWAP_API_KEY"
#             swapped_images = []
            
#             for img_base64 in generated_images:
#                 swapped_image = apply_faceswap(face_image_base64, img_base64, faceswap_api_key)
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
#                         st.image(image, use_column_width=True)
#         else:
#             st.error("Failed to generate outfit suggestions.")
#     else:
#         st.error("Please fill in all the details and upload your face image.")




# import streamlit as st
# import requests
# import base64
# from PIL import Image
# from io import BytesIO

# # Helper functions for image handling
# def image_file_to_base64(image_path):
#     with open(image_path, "rb") as f:
#         image_data = f.read()
#     return base64.b64encode(image_data).decode("utf-8")

# def image_to_base64(image):
#     return base64.b64encode(image.read()).decode("utf-8")

# def decode_base64_to_image(base64_data):
#     return Image.open(BytesIO(base64.b64decode(base64_data)))

# # Updated generate_outfits function with troubleshooting
# def generate_outfits(prompt, api_key):
#     url = "https://api.segmind.com/v1/stable-diffusion-3.5-large-txt2img"
#     headers = {'x-api-key': "SG_b10384629aa194e1"}
#     data = {
#         "prompt": prompt,
#         "negative_prompt": "low quality, blurry",
#         "steps": 25,
#         "guidance_scale": 5.5,
#         "seed": 98552302,
#         "sampler": "euler",
#         "scheduler": "sgm_uniform",
#         "width": 512,
#         "height": 512,
#         "batch_size": 4,
#         "image_format": "jpeg",
#         "base64": True  # Use base64 encoded images for simplicity
#     }

#     response = requests.post(url, json=data, headers=headers)
    
#     # Log response for debugging
#     st.write("API Response Status Code:", response.status_code)
#     try:
#         st.write("API Response JSON:", response.json())
#     except Exception as e:
#         st.error(f"Failed to parse API response as JSON. Error: {e}")
#         return []

#     # Handle non-200 status codes
#     if response.status_code != 200:
#         st.error("Error in API request. Please check your API key and request payload.")
#         return []
    
#     # Safeguard against missing "images" key in response
#     response_json = response.json()
#     if "images" in response_json:
#         return response_json["images"]
#     else:
#         st.error("API response did not contain 'images'. Check the API documentation or response structure.")
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
#     headers = {"x-api-key": "SG_b10384629aa194e1"}
#     response = requests.post(url, json=data, headers=headers)
    
#     if response.status_code == 200:
#         return response.json()["image"]
#     else:
#         st.error("Error applying FaceSwap. Please try again.")
#         return None

# # Streamlit UI
# st.title("Personalized Outfit Suggester")
# st.write("Upload your face image and fill in your details to get personalized outfit suggestions.")

# # User inputs
# body_type = st.selectbox("Body Type", ["Select your body type", "Slim", "Athletic", "Curvy", "Plus Size"])
# body_shape = st.selectbox("Body Shape", ["Select your body shape", "Rectangle", "Hourglass", "Triangle", "Inverted Triangle"])
# gender = st.selectbox("Gender", ["Select your gender", "Male", "Female", "Non-Binary"])
# color_complexion = st.selectbox("Color Complexion", ["Select your color complexion", "Light", "Medium", "Dark"])
# uploaded_file = st.file_uploader("Your Face Image", type=["png", "jpg", "jpeg"])

# # Button to generate outfits
# if st.button("Generate Outfit Suggestions"):
#     if uploaded_file and body_type != "Select your body type" and body_shape != "Select your body shape" and gender != "Select your gender" and color_complexion != "Select your color complexion":
#         st.info("Processing... This might take a few seconds.")
        
#         # Convert uploaded file to base64
#         face_image_base64 = image_to_base64(uploaded_file)
        
#         # Generate outfit images using Text-to-Image API
#         st.info("Generating outfit suggestions...")
#         text_to_image_api_key = "YOUR_TEXT_TO_IMAGE_API_KEY"
#         prompt = f"A {gender.lower()} with a {body_type.lower()} body and {color_complexion.lower()} complexion wearing stylish outfits."
#         generated_images = generate_outfits(prompt, text_to_image_api_key)
        
#         if generated_images:
#             st.info("Applying FaceSwap to the generated outfits...")
#             faceswap_api_key = "YOUR_FACESWAP_API_KEY"
#             swapped_images = []
            
#             for img_base64 in generated_images:
#                 swapped_image = apply_faceswap(face_image_base64, img_base64, faceswap_api_key)
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
#                         st.image(image, use_column_width=True)
#         else:
#             st.error("Failed to generate outfit suggestions.")
#     else:
#         st.error("Please fill in all the details and upload your face image.")





# import streamlit as st
# import requests
# import base64
# from PIL import Image
# from io import BytesIO

# # Helper functions for image handling
# def image_file_to_base64(image_path):
#     with open(image_path, "rb") as f:
#         image_data = f.read()
#     return base64.b64encode(image_data).decode("utf-8")

# def image_to_base64(image):
#     return base64.b64encode(image.read()).decode("utf-8")

# def decode_base64_to_image(base64_data):
#     return Image.open(BytesIO(base64.b64decode(base64_data)))

# # Updated generate_outfits function
# def generate_outfits(prompt, api_key):
#     url = "https://api.segmind.com/v1/stable-diffusion-3.5-large-txt2img"
#     headers = {'x-api-key': "SG_b10384629aa194e1"}
#     data = {
#         "prompt": prompt,
#         "negative_prompt": "low quality, blurry",
#         "steps": 25,
#         "guidance_scale": 5.5,
#         "seed": 98552302,
#         "sampler": "euler",
#         "scheduler": "sgm_uniform",
#         "width": 512,
#         "height": 512,
#         "batch_size": 4,
#         "image_format": "jpeg",
#         "base64": True  # Use base64 encoded images for simplicity
#     }

#     response = requests.post(url, json=data, headers=headers)
    
#     # Log response for debugging
#     st.write("API Response Status Code:", response.status_code)
#     try:
#         st.write("API Response JSON:", response.json())
#     except Exception as e:
#         st.error(f"Failed to parse API response as JSON. Error: {e}")
#         return []

#     # Handle non-200 status codes
#     if response.status_code != 200:
#         st.error("Error in API request. Please check your API key and request payload.")
#         return []
    
#     # Handle the correct key from the API response
#     response_json = response.json()
#     if "image" in response_json:  # Check for "image" instead of "images"
#         return response_json["image"]  # Return the list of images
#     else:
#         st.error("API response did not contain 'image'. Check the API documentation or response structure.")
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
#     headers = {"x-api-key": "SG_b10384629aa194e1"}
#     response = requests.post(url, json=data, headers=headers)
    
#     if response.status_code == 200:
#         return response.json()["image"]
#     else:
#         st.error("Error applying FaceSwap. Please try again.")
#         return None

# # Streamlit UI
# st.title("Personalized Outfit Suggester")
# st.write("Upload your face image and fill in your details to get personalized outfit suggestions.")

# # User inputs
# body_type = st.selectbox("Body Type", ["Select your body type", "Slim", "Athletic", "Curvy", "Plus Size"])
# body_shape = st.selectbox("Body Shape", ["Select your body shape", "Rectangle", "Hourglass", "Triangle", "Inverted Triangle"])
# gender = st.selectbox("Gender", ["Select your gender", "Male", "Female", "Non-Binary"])
# color_complexion = st.selectbox("Color Complexion", ["Select your color complexion", "Light", "Medium", "Dark"])
# uploaded_file = st.file_uploader("Your Face Image", type=["png", "jpg", "jpeg"])

# # Button to generate outfits
# if st.button("Generate Outfit Suggestions"):
#     if uploaded_file and body_type != "Select your body type" and body_shape != "Select your body shape" and gender != "Select your gender" and color_complexion != "Select your color complexion":
#         st.info("Processing... This might take a few seconds.")
        
#         # Convert uploaded file to base64
#         face_image_base64 = image_to_base64(uploaded_file)
        
#         # Generate outfit images using Text-to-Image API
#         st.info("Generating outfit suggestions...")
#         text_to_image_api_key = "YOUR_TEXT_TO_IMAGE_API_KEY"
#         prompt = f"A {gender.lower()} with a {body_type.lower()} body and {color_complexion.lower()} complexion wearing stylish outfits."
#         generated_images = generate_outfits(prompt, text_to_image_api_key)
        
#         if generated_images:
#             st.info("Applying FaceSwap to the generated outfits...")
#             faceswap_api_key = "YOUR_FACESWAP_API_KEY"
#             swapped_images = []
            
#             for img_base64 in generated_images:
#                 swapped_image = apply_faceswap(face_image_base64, img_base64, faceswap_api_key)
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
#                         st.image(image, use_column_width=True)
#         else:
#             st.error("Failed to generate outfit suggestions.")
#     else:
#         st.error("Please fill in all the details and upload your face image.")





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
        generated_images = generate_outfits(prompt, text_to_image_api_key)
        
        if generated_images:
            st.info("Applying FaceSwap to the generated outfits...")
            swapped_images = []
            
            for img_base64 in generated_images:
                swapped_image = apply_faceswap(face_image_base64, img_base64, faceswap_api_key)
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
