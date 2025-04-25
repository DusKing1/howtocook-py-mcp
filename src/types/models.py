from pydantic import BaseModel
from typing import List, Optional, Dict

# 定义菜谱的类型接口
class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    text_quantity: str
    notes: Optional[str] = ""

class Step(BaseModel):
    step: int
    description: str

class Recipe(BaseModel):
    id: str
    name: str
    description: str
    source_path: str
    image_path: Optional[str] = None
    category: str
    difficulty: int
    tags: List[str]
    servings: int
    ingredients: List[Ingredient]
    steps: List[Step]
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    total_time_minutes: Optional[int] = None
    additional_notes: List[str] = []

# 添加简化版的Recipe接口，只包含id、name和description
class SimpleRecipe(BaseModel):
    id: str
    name: str
    description: str
    ingredients: List[Dict[str, str]]

# 更简化的Recipe接口，只包含name和description，用于getAllRecipes
class NameOnlyRecipe(BaseModel):
    name: str
    description: str

# 定义膳食计划相关接口
class DayPlan(BaseModel):
    day: str
    breakfast: List[SimpleRecipe]
    lunch: List[SimpleRecipe]
    dinner: List[SimpleRecipe]

class ShoppingPlanCategories(BaseModel):
    fresh: List[str] = []
    pantry: List[str] = []
    spices: List[str] = []
    others: List[str] = []

class GroceryItem(BaseModel):
    name: str
    total_quantity: Optional[float] = None
    unit: Optional[str] = None
    recipe_count: int
    recipes: List[str]

class GroceryList(BaseModel):
    ingredients: List[GroceryItem] = []
    shopping_plan: ShoppingPlanCategories = ShoppingPlanCategories()

class MealPlan(BaseModel):
    weekdays: List[DayPlan] = []
    weekend: List[DayPlan] = []
    grocery_list: GroceryList = GroceryList()

# 定义推荐菜品的接口
class DishRecommendation(BaseModel):
    people_count: int
    meat_dish_count: int
    vegetable_dish_count: int
    dishes: List[SimpleRecipe]
    message: str 