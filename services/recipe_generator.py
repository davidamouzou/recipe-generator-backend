import base64
import io
import json
from google import genai
from PIL import Image  # Pillow library for image manipulation
from config import config
from typing import Tuple


# format of the response from the model (valid JSON example with concrete placeholders)
response_format = '''
{
    "recipe_name": "",
    "diet": "",
    "continent": "",
    "language": "",
    "ingredients": [""],
    "duration_to_cook": 0,
    "servings": 0,
    "instructions": [""],
    "difficulty": "",
    "cuisine": "",
    "description": "",
    "meal_type": "",
    "image": "",
    "nutrition_facts": {
        "calories": "",
        "protein": "",
        "carbohydrates": "",
        "fat": "",
        "vitamins": "",
        "minerals": "",
        "dietary_fiber": "",
        "sugar": "",
        "salt": "",
        "antioxidants": ""
    }
}
'''


def smart_json_encode(text: str) -> dict:
    # Remove common markdown fences and surrounding noise, then extract the first JSON object/array found.
    if not isinstance(text, str):
        raise ValueError("Response text is not a string")

    cleaned = text.replace("```json", "").replace("```", "").strip()

    # Find the start of the JSON (either object or array)
    start_idx = None
    for i, ch in enumerate(cleaned):
        if ch in ("{", "["):
            start_idx = i
            break

    if start_idx is None:
        raise ValueError("No JSON object or array found in response")

    open_char = cleaned[start_idx]
    close_char = "}" if open_char == "{" else "]"

    # Find the last matching closing character
    end_idx = cleaned.rfind(close_char)
    if end_idx == -1 or end_idx <= start_idx:
        raise ValueError("No closing JSON bracket found in response")

    json_text = cleaned[start_idx:end_idx + 1]
    obj = json.loads(json_text)

    return obj


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

    return smart_json_encode(response.text)