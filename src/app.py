#!/usr/bin/env python
import asyncio
import os
from mcp.server import FastMCP

from .data.recipes import fetch_recipes, get_all_categories

# 创建MCP服务器
app = FastMCP(
    name="howtocook-py-mcp",
    version="0.0.1",
    description="菜谱助手 MCP 服务",
    port=9000
)

# 获取所有菜谱工具
@app.tool()
async def get_all_recipes():
    """
    获取所有菜谱

    Returns:
        所有菜谱的简化信息，只包含名称和描述
    """
    # 获取菜谱数据
    from .utils.recipe_utils import simplify_recipe_name_only
    
    recipes = await fetch_recipes()
    if not recipes:
        return "未能获取菜谱数据"
    
    # 返回更简化版的菜谱数据，只包含name和description
    simplified_recipes = [simplify_recipe_name_only(recipe) for recipe in recipes]
    
    # 返回JSON字符串
    import json
    return json.dumps([recipe.model_dump() for recipe in simplified_recipes], 
                     ensure_ascii=False, indent=2)

# 按分类获取菜谱工具
@app.tool()
async def get_recipes_by_category(category: str):
    """
    根据分类查询菜谱
    
    Args:
        category: 菜谱分类名称，如水产、早餐、荤菜、主食等
        
    Returns:
        该分类下所有菜谱的简化信息
    """
    from .utils.recipe_utils import simplify_recipe
    
    recipes = await fetch_recipes()
    if not recipes:
        return "未能获取菜谱数据"
    
    # 过滤出指定分类的菜谱
    filtered_recipes = [recipe for recipe in recipes if recipe.category == category]
    
    # 返回简化版的菜谱数据
    simplified_recipes = [simplify_recipe(recipe) for recipe in filtered_recipes]
    
    # 返回JSON字符串
    import json
    return json.dumps([recipe.model_dump() for recipe in simplified_recipes], 
                     ensure_ascii=False, indent=2)

# 不知道吃什么推荐工具
@app.tool()
async def what_to_eat(people_count: int):
    """
    不知道吃什么？根据人数直接推荐适合的菜品组合
    
    Args:
        people_count: 用餐人数，1-10之间的整数，会根据人数推荐合适数量的菜品
        
    Returns:
        推荐的菜品组合，包含荤菜和素菜
    """
    import random
    from .utils.recipe_utils import simplify_recipe
    from .types.models import DishRecommendation
    
    recipes = await fetch_recipes()
    if not recipes:
        return "未能获取菜谱数据"
        
    # 根据人数计算荤素菜数量
    vegetable_count = (people_count + 1) // 2
    meat_count = (people_count + 1) // 2 + (people_count + 1) % 2
    
    # 获取所有荤菜
    meat_dishes = [
        recipe for recipe in recipes
        if recipe.category == '荤菜' or recipe.category == '水产'
    ]
    
    # 获取其他可能的菜品（当做素菜）
    vegetable_dishes = [
        recipe for recipe in recipes
        if recipe.category not in ['荤菜', '水产', '早餐', '主食']
    ]
    
    # 特别处理：如果人数超过8人，增加鱼类荤菜
    recommended_dishes = []
    fish_dish = None
    
    if people_count > 8:
        fish_dishes = [recipe for recipe in recipes if recipe.category == '水产']
        if fish_dishes:
            fish_dish = random.choice(fish_dishes)
            recommended_dishes.append(fish_dish)
    
    # 按照不同肉类的优先级选择荤菜
    meat_types = ['猪肉', '鸡肉', '牛肉', '羊肉', '鸭肉', '鱼肉']
    selected_meat_dishes = []
    
    # 需要选择的荤菜数量
    remaining_meat_count = meat_count - (1 if fish_dish else 0)
    
    # 尝试按照肉类优先级选择荤菜
    for meat_type in meat_types:
        if len(selected_meat_dishes) >= remaining_meat_count:
            break
        
        meat_type_options = [
            dish for dish in meat_dishes
            if any(
                meat_type.lower() in (ingredient.name or "").lower()
                for ingredient in dish.ingredients
            )
        ]
        
        if meat_type_options:
            # 随机选择一道这种肉类的菜
            selected = random.choice(meat_type_options)
            selected_meat_dishes.append(selected)
            # 从可选列表中移除，避免重复选择
            meat_dishes = [dish for dish in meat_dishes if dish.id != selected.id]
    
    # 如果通过肉类筛选的荤菜不够，随机选择剩余的
    while len(selected_meat_dishes) < remaining_meat_count and meat_dishes:
        random_dish = random.choice(meat_dishes)
        selected_meat_dishes.append(random_dish)
        meat_dishes.remove(random_dish)
    
    # 随机选择素菜
    selected_vegetable_dishes = []
    while len(selected_vegetable_dishes) < vegetable_count and vegetable_dishes:
        random_dish = random.choice(vegetable_dishes)
        selected_vegetable_dishes.append(random_dish)
        vegetable_dishes.remove(random_dish)
    
    # 合并推荐菜单
    recommended_dishes.extend(selected_meat_dishes)
    recommended_dishes.extend(selected_vegetable_dishes)
    
    # 构建推荐结果
    dish_recommendation = DishRecommendation(
        people_count=people_count,
        meat_dish_count=len(selected_meat_dishes) + (1 if fish_dish else 0),
        vegetable_dish_count=len(selected_vegetable_dishes),
        dishes=[simplify_recipe(dish) for dish in recommended_dishes],
        message=f"为{people_count}人推荐的菜品，包含{len(selected_meat_dishes) + (1 if fish_dish else 0)}个荤菜和{len(selected_vegetable_dishes)}个素菜。"
    )
    
    # 返回JSON字符串
    import json
    return json.dumps(dish_recommendation.model_dump(), ensure_ascii=False, indent=2)

# 推荐膳食计划工具
@app.tool()
async def recommend_meals(people_count: int, allergies: list = None, avoid_items: list = None):
    """
    根据用户的忌口、过敏原、人数智能推荐菜谱，创建一周的膳食计划以及大致的购物清单
    
    Args:
        people_count: 用餐人数，1-10之间的整数
        allergies: 过敏原列表，如['大蒜', '虾']
        avoid_items: 忌口食材列表，如['葱', '姜']
        
    Returns:
        一周的膳食计划以及大致的购物清单
    """
    import random
    import json
    from .utils.recipe_utils import (
        simplify_recipe,
        process_recipe_ingredients,
        categorize_ingredients
    )
    from .types.models import MealPlan, DayPlan, GroceryItem
    
    if allergies is None:
        allergies = []
    if avoid_items is None:
        avoid_items = []
    
    recipes = await fetch_recipes()
    if not recipes:
        return "未能获取菜谱数据"
    
    # 过滤掉含有忌口和过敏原的菜谱
    filtered_recipes = []
    for recipe in recipes:
        # 检查是否包含过敏原或忌口食材
        has_allergies_or_avoid_items = False
        for ingredient in recipe.ingredients:
            ingredient_name = ingredient.name.lower()
            if any(allergy.lower() in ingredient_name for allergy in allergies) or \
               any(item.lower() in ingredient_name for item in avoid_items):
                has_allergies_or_avoid_items = True
                break
        
        if not has_allergies_or_avoid_items:
            filtered_recipes.append(recipe)
    
    # 将菜谱按分类分组
    recipes_by_category = {}
    target_categories = ['水产', '早餐', '荤菜', '主食']
    
    for recipe in filtered_recipes:
        if recipe.category in target_categories:
            if recipe.category not in recipes_by_category:
                recipes_by_category[recipe.category] = []
            recipes_by_category[recipe.category].append(recipe)
    
    # 创建每周膳食计划
    meal_plan = MealPlan()
    
    # 用于跟踪已经选择的菜谱，以便后续处理食材信息
    selected_recipes = []
    
    # 周一至周五
    for i in range(5):
        day_plan = DayPlan(
            day=['周一', '周二', '周三', '周四', '周五'][i],
            breakfast=[],
            lunch=[],
            dinner=[]
        )
    
        # 早餐 - 根据人数推荐1-2个早餐菜单
        breakfast_count = max(1, (people_count + 4) // 5)
        if '早餐' in recipes_by_category and recipes_by_category['早餐']:
            for _ in range(breakfast_count):
                if not recipes_by_category['早餐']:
                    break
                breakfast_index = random.randrange(len(recipes_by_category['早餐']))
                selected_recipe = recipes_by_category['早餐'][breakfast_index]
                selected_recipes.append(selected_recipe)
                day_plan.breakfast.append(simplify_recipe(selected_recipe))
                # 避免重复，从候选列表中移除
                recipes_by_category['早餐'].pop(breakfast_index)
    
        # 午餐和晚餐的菜谱数量，根据人数确定
        meal_count = max(2, (people_count + 2) // 3)
        
        # 午餐
        for _ in range(meal_count):
            # 随机选择菜系：主食、水产、蔬菜、荤菜等
            categories = ['主食', '水产', '荤菜', '素菜', '甜品']
            
            # 随机选择一个分类
            while True:
                if not categories:
                    break
                    
                selected_category = random.choice(categories)
                categories.remove(selected_category)
                
                if selected_category in recipes_by_category and recipes_by_category[selected_category]:
                    index = random.randrange(len(recipes_by_category[selected_category]))
                    selected_recipe = recipes_by_category[selected_category][index]
                    selected_recipes.append(selected_recipe)
                    day_plan.lunch.append(simplify_recipe(selected_recipe))
                    # 避免重复，从候选列表中移除
                    recipes_by_category[selected_category].pop(index)
                    break
        
        # 晚餐
        for _ in range(meal_count):
            # 随机选择菜系，与午餐类似但可添加汤羹
            categories = ['主食', '水产', '荤菜', '素菜', '甜品', '汤羹']
            
            # 随机选择一个分类
            while True:
                if not categories:
                    break
                    
                selected_category = random.choice(categories)
                categories.remove(selected_category)
                
                if selected_category in recipes_by_category and recipes_by_category[selected_category]:
                    index = random.randrange(len(recipes_by_category[selected_category]))
                    selected_recipe = recipes_by_category[selected_category][index]
                    selected_recipes.append(selected_recipe)
                    day_plan.dinner.append(simplify_recipe(selected_recipe))
                    # 避免重复，从候选列表中移除
                    recipes_by_category[selected_category].pop(index)
                    break
    
        meal_plan.weekdays.append(day_plan)
    
    # 周六和周日处理逻辑...（此处省略部分代码）
    # 统计食材清单...（此处省略部分代码）
    
    # 返回JSON字符串
    return json.dumps(meal_plan.model_dump(), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    app.run(transport='sse')
