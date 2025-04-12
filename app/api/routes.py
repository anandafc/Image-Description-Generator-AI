from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.gemini import GeminiService
import json

router = APIRouter(prefix="/api", tags=["image"])
gemini_service = GeminiService()

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed")
        image_bytes = await file.read()
        result = gemini_service.analyze_image(image_bytes)
        try:
            cleaned_result = result.strip()
            if cleaned_result.startswith("```json"):
                cleaned_result = cleaned_result.strip("```json").strip("```").strip()
            elif cleaned_result.startswith("```"):
                cleaned_result = cleaned_result.strip("```").strip()
            return json.loads(cleaned_result)
        except json.JSONDecodeError:
            return {"error": "Invalid response format from Gemini", "raw_response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))