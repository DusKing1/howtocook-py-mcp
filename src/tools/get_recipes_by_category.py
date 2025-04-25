import json
from typing import List
from fastmcp import McpServer, z
from ..types.models import Recipe
from ..utils.recipe_utils import simplify_recipe

def register_get_recipes_by_category_tool(
    server: McpServer, 
    recipes: List[Recipe], 
    categories: List[str]
):
    """注册按分类获取菜谱工具
    
    Args:
        server: MCP服务器实例
        recipes: 菜谱列表
        categories: 分类列表
    """
    @server.tool(
        name="mcp_howtocook_getRecipesByCategory",
        description=f"根据分类查询菜谱，可选分类有: {', '.join(categories)}",
        params={
            "category": z.enum(categories, description="菜谱分类名称，如水产、早餐、荤菜、主食等")
        },
    )
    async def get_recipes_by_category(category: str):
        filtered_recipes = [recipe for recipe in recipes if recipe.category == category]
        # 返回简化版的菜谱数据
        simplified_recipes = [simplify_recipe(recipe) for recipe in filtered_recipes]
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        [recipe.model_dump() for recipe in simplified_recipes], 
                        ensure_ascii=False, 
                        indent=2
                    ),
                },
            ],
        } 