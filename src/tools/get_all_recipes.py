import json
from typing import List
from fastmcp import McpServer
from ..types.models import Recipe
from ..utils.recipe_utils import simplify_recipe_name_only

def register_get_all_recipes_tool(server: McpServer, recipes: List[Recipe]):
    """注册获取所有菜谱工具
    
    Args:
        server: MCP服务器实例
        recipes: 菜谱列表
    """
    @server.tool(
        name="mcp_howtocook_getAllRecipes",
        description="获取所有菜谱",
        params={},
    )
    async def get_all_recipes():
        # 返回更简化版的菜谱数据，只包含name和description
        simplified_recipes = [simplify_recipe_name_only(recipe) for recipe in recipes]
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