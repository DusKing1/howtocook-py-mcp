from typing import Dict, List, Mapping, Optional, Set, Any
from ..types.models import (
    Recipe, 
    SimpleRecipe, 
    NameOnlyRecipe,
    GroceryItem,
    ShoppingPlanCategories
)

# 创建简化版的Recipe数据
def simplify_recipe(recipe: Recipe) -> SimpleRecipe:
    return SimpleRecipe(
        id=recipe.id,
        name=recipe.name,
        description=recipe.description,
        ingredients=[{
            "name": ingredient.name,
            "text_quantity": ingredient.text_quantity
        } for ingredient in recipe.ingredients]
    )

# 创建只包含name和description的Recipe数据
def simplify_recipe_name_only(recipe: Recipe) -> NameOnlyRecipe:
    return NameOnlyRecipe(
        name=recipe.name,
        description=recipe.description
    )

# 处理食材清单，收集菜谱的所有食材
def process_recipe_ingredients(
    recipe: Recipe, 
    ingredient_map: Dict[str, GroceryItem]
) -> None:
    for ingredient in recipe.ingredients:
        key = ingredient.name.lower()
        
        if key not in ingredient_map:
            ingredient_map[key] = GroceryItem(
                name=ingredient.name,
                total_quantity=ingredient.quantity,
                unit=ingredient.unit,
                recipe_count=1,
                recipes=[recipe.name]
            )
        else:
            existing = ingredient_map[key]
            
            # 对于有明确数量和单位的食材，进行汇总
            if (existing.unit and ingredient.unit and existing.unit == ingredient.unit 
                    and existing.total_quantity is not None and ingredient.quantity is not None):
                existing.total_quantity += ingredient.quantity
            else:
                # 否则保留 None，表示数量不确定
                existing.total_quantity = None
                existing.unit = None
            
            existing.recipe_count += 1
            if recipe.name not in existing.recipes:
                existing.recipes.append(recipe.name)

# 根据食材类型进行分类
def categorize_ingredients(
    ingredients: List[GroceryItem], 
    shopping_plan: ShoppingPlanCategories
) -> None:
    spice_keywords = [
        '盐', '糖', '酱油', '醋', '料酒', '香料', '胡椒', '孜然', 
        '辣椒', '花椒', '姜', '蒜', '葱', '调味'
    ]
    fresh_keywords = [
        '肉', '鱼', '虾', '蛋', '奶', '菜', '菠菜', '白菜', '青菜',
        '豆腐', '生菜', '水产', '豆芽', '西红柿', '番茄', '水果',
        '香菇', '木耳', '蘑菇'
    ]
    pantry_keywords = [
        '米', '面', '粉', '油', '酒', '醋', '糖', '盐', '酱', '豆',
        '干', '罐头', '方便面', '面条', '米饭', '意大利面', '燕麦'
    ]

    for ingredient in ingredients:
        name = ingredient.name.lower()
        
        if any(keyword in name for keyword in spice_keywords):
            shopping_plan.spices.append(ingredient.name)
        elif any(keyword in name for keyword in fresh_keywords):
            shopping_plan.fresh.append(ingredient.name)
        elif any(keyword in name for keyword in pantry_keywords):
            shopping_plan.pantry.append(ingredient.name)
        else:
            shopping_plan.others.append(ingredient.name) 