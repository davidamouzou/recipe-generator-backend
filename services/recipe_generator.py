import base64
import io
import json
from google import genai
from PIL import Image  # Pillow library for image manipulation
from config import config
from models import response_format
    

# Generate a recipe based on a description
def generate_recipe_by_description(data) -> dict:
    # Configuration of the Gemini model
    client = genai.Client(api_key=config.get("model_api_key"))

    list_file = []
    if data['files']:
        # Convert the base64 string to image
        for imageBase in data['files']:
            img_data = base64.b64decode(imageBase['base64'])
            image = Image.open(io.BytesIO(img_data))
            list_file.append(image)

    prompt = f"""
    Analyze the following user input: "{data['text']}" and return an appropriate response in {data['language']}:
    1. If the input is not related to ingredients or a dish, return the following response in JSON format:
    {{"message": "", "data": []}}.
    2. If the input is relevant and describes specific ingredients or a dish, return a corresponding recipe in the form of a JSON object:
    {{"message": "", "data": [{response_format}]}}.
    Note: The response must be formulated in the language {data['language']} and should be only JSON, not any other message.
    """
    response = client.models.generate_content(model="gemini-2.5-flash", contents=[prompt, *list_file])
    client.close()

    cleaned = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)