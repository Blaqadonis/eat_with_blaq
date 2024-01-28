import gradio as gr
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai
from io import BytesIO

# Load environment variables
load_dotenv()  # Uncomment this if you are using a .env file to store your API key

# Configure the Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_image):
    if uploaded_image is not None:
        # Convert the uploaded image to bytes
        bytes_data = BytesIO()

        # Get the format of the uploaded image, default to JPEG if not found
        image_format = uploaded_image.format or 'JPEG'

        uploaded_image.save(bytes_data, format=image_format)
        bytes_data = bytes_data.getvalue()

        image_parts = [
            {
                "mime_type": f"image/{image_format.lower()}",  # Use the format to set mime type
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def process(input, uploaded_image):
    input_prompt = """
    You are an expert in nutrition where you need to see the food items from the image
    and calculate the total calories, also provide the details of every food items with calories intake
    in the below format:

    1. Item 1 - no of calories
    2. Item 2 - no of calories
    ----
    ----
    Finally, you can also mention if the food is healthy or not.
    """
    if uploaded_image is not None:
        image_data = input_image_setup(uploaded_image)
        response = get_gemini_response(input_prompt, image_data, input)
        return response
    else:
        return "Please upload an image."

# Define the Gradio interface
iface = gr.Interface(
    fn=process,
    inputs=[
        gr.Textbox(label="Input Prompt", value="You are an expert in nutrition where you need to see the food items from the image and calculate the total calories."),
        gr.Image(type="pil", label="Upload Image")
    ],
    outputs="text",
    title="Eat with 🅱🅻🅰🆀",
    description="Ask 🅱🅻🅰🆀 about your diet and get an expert's opinion.",
    theme=gr.themes.Soft(),
    allow_flagging="never"
)

iface.launch(debug=True, share=True)