import json
import random
from typing import Dict, List
from fastmcp import McpServer, z
from ..types.models import (
    Recipe, 
    MealPlan, 
    DayPlan, 
    GroceryList, 
    GroceryItem,
    ShoppingPlanCategories
)
from ..utils.recipe_utils import (
    simplify_recipe, 
    process_recipe_ingredients,
    categorize_ingredients
)

def register_recommend_meals_tool(server: McpServer, recipes: List[Recipe]):
    """注册推荐膳食和购物清单工具
    
    Args:
        server: MCP服务器实例
        recipes: 菜谱列表
    """
    @server.tool(
        name="mcp_howtocook_recommendMeals",
        description="根据用户的忌口、过敏原、人数智能推荐菜谱，创建一周的膳食计划以及大致的购物清单",
        params={
            "allergies": z.array(
                z.string(description="过敏原，例如'大蒜'")
            ).optional().describe("过敏原列表，如['大蒜', '虾']"),
            "avoid_items": z.array(
                z.string(description="忌口食材，例如'葱'")
            ).optional().describe("忌口食材列表，如['葱', '姜']"),
            "people_count": z.number(
                description="用餐人数，1-10之间的整数"
            ).int().min(1).max(10)
        },
    )
    async def recommend_meals(
        people_count: int,
        allergies: List[str] = None, 
        avoid_items: List[str] = None
    ):
        if allergies is None:
            allergies = []
        if avoid_items is None:
            avoid_items = []
            
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
        recipes_by_category: Dict[str, List[Recipe]] = {}
        target_categories = ['水产', '早餐', '荤菜', '主食']
        
        for recipe in filtered_recipes:
            if recipe.category in target_categories:
                if recipe.category not in recipes_by_category:
                    recipes_by_category[recipe.category] = []
                recipes_by_category[recipe.category].append(recipe)

        # 创建每周膳食计划
        meal_plan = MealPlan()

        # 用于跟踪已经选择的菜谱，以便后续处理食材信息
        selected_recipes: List[Recipe] = []

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

        # 周六和周日
        for i in range(2):
            day_plan = DayPlan(
                day=['周六', '周日'][i],
                breakfast=[],
                lunch=[],
                dinner=[]
            )

            # 早餐 - 根据人数推荐菜品，至少2个菜品，随人数增加
            breakfast_count = max(2, (people_count + 2) // 3)
            if '早餐' in recipes_by_category and recipes_by_category['早餐']:
                for _ in range(breakfast_count):
                    if not recipes_by_category['早餐']:
                        break
                    breakfast_index = random.randrange(len(recipes_by_category['早餐']))
                    selected_recipe = recipes_by_category['早餐'][breakfast_index]
                    selected_recipes.append(selected_recipe)
                    day_plan.breakfast.append(simplify_recipe(selected_recipe))
                    recipes_by_category['早餐'].pop(breakfast_index)

            # 计算工作日的基础菜品数量
            weekday_meal_count = max(2, (people_count + 2) // 3)
            # 周末菜品数量：比工作日多1-2个菜，随人数增加
            weekend_addition = 1 if people_count <= 4 else 2 # 4人以下多1个菜，4人以上多2个菜
            meal_count = weekday_meal_count + weekend_addition

            def get_meals(count: int):
                result = []
                categories = ['荤菜', '水产'] + ['主食'] * 3  # 增加主食被选中的概率
                
                for _ in range(count):
                    if not categories:
                        break
                        
                    random.shuffle(categories)  # 随机打乱分类顺序
                    
                    selected = False
                    for category in categories[:]:
                        if category in recipes_by_category and recipes_by_category[category]:
                            index = random.randrange(len(recipes_by_category[category]))
                            selected_recipe = recipes_by_category[category][index]
                            selected_recipes.append(selected_recipe)
                            result.append(simplify_recipe(selected_recipe))
                            recipes_by_category[category].pop(index)
                            selected = True
                            break
                    
                    if not selected:
                        # 如果所有分类都没有菜品了，尝试使用过滤前的菜谱
                        other_categories = [c for c in recipes_by_category if recipes_by_category[c]]
                        if other_categories:
                            category = random.choice(other_categories)
                            index = random.randrange(len(recipes_by_category[category]))
                            selected_recipe = recipes_by_category[category][index]
                            selected_recipes.append(selected_recipe)
                            result.append(simplify_recipe(selected_recipe))
                            recipes_by_category[category].pop(index)
                
                return result

            day_plan.lunch = get_meals(meal_count)
            day_plan.dinner = get_meals(meal_count)

            meal_plan.weekend.append(day_plan)

        # 统计食材清单，收集所有菜谱的所有食材
        ingredient_map: Dict[str, GroceryItem] = {}
        
        for recipe in selected_recipes:
            process_recipe_ingredients(recipe, ingredient_map)
        
        # 将食材添加到购物清单
        meal_plan.grocery_list.ingredients = list(ingredient_map.values())
        
        # 根据食材类型分类食材
        categorize_ingredients(
            meal_plan.grocery_list.ingredients,
            meal_plan.grocery_list.shopping_plan
        )
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        meal_plan.model_dump(), 
                        ensure_ascii=False, 
                        indent=2
                    ),
                },
            ],
        } 