from datetime import datetime
from pydantic import BaseModel


class Recipe(BaseModel):
    created_at: datetime = datetime.now()
    recipe_name: str
    ingredients: list[str]  # ingredients to compose recipe
    instructions: list[str]
    continent: str
    language: str
    duration_to_cook: int
    servings: int
    difficulty: str
    cuisine: str
    description: str
    meal_type: str
    nutrition_facts: dict  # No description
    image: str = ""