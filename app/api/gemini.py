import google.generativeai as genai
from PIL import Image
import io
from app.config import config

class GeminiService:
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def analyze_image(self, image_bytes: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            prompt = (
                "Analyze the image and return a valid JSON object with:\n"
                "- 'colors': array of dominant colors (e.g., ['red', 'blue']),\n"
                "- 'objects': array of detected objects (e.g., ['tree', 'car']),\n"
                "- 'ambiance': mood or atmosphere (e.g., 'calm', 'vibrant'),\n"
                "- 'description': brief image description with a sarcastic approach (max 50 words, e.g., 'A serene lake with blue water and green trees under a clear sky.').\n"
                "Example: {\"colors\": [\"blue\", \"green\"], \"objects\": [\"lake\", \"trees\"], \"ambiance\": \"calm\", \"description\": \"A serene lake with blue water and green trees under a clear sky.\"}"
            )
            response = self.model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            return f'{{"error": "{str(e)}"}}'