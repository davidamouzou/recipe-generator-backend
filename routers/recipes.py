import json
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config import supabase_client
from models.recipe import Recipe
from services.upload_url_image import save_image


recipe_table = supabase_client.table("recipes")
router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/add")
def save(recipe: Recipe):
    try:
        json_data = recipe.model_dump()
        res = recipe_table.insert(json_data).execute()
        return res.data
    except Exception as e:
        return JSONResponse(status_code=503, content=f"Error: {e}")


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    try:
        res = recipe_table.select("*").eq('id', recipe_id).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        return JSONResponse(status_code=503, content=f"Error: {e}")


@router.get("/")
def get_all(offset: int = 0, limit: int = 10):
    if (limit - offset) > 10:
        limit = offset + 10

    try:
        response = recipe_table.select('*').range(offset, limit).order('id', desc=True).execute()
        return response.data
    except Exception as e:
        return JSONResponse(status_code=503, content=f"Error: {e}")


@router.post("/upload_image")
async def upload_image(req: Request):
    data = await req.json()
    try:
        res = save_image(url=data['url'], bucket="recipe-gen-images")
        return res
    except Exception as e:
        return JSONResponse(status_code=503, content=f"Error: {e}")