import httpx
from typing import List
from ..types.models import Recipe

# 远程菜谱JSON文件URL
RECIPES_URL = 'https://mp-bc8d1f0a-3356-4a4e-8592-f73a3371baa2.cdn.bspapp.com/all_recipes.json'

# 从远程URL获取数据的异步函数
async def fetch_recipes() -> List[Recipe]:
    try:
        # 使用httpx异步获取远程数据
        async with httpx.AsyncClient() as client:
            response = await client.get(RECIPES_URL)
            
            if response.status_code != 200:
                raise Exception(f"HTTP error! Status: {response.status_code}")
            
            # 解析JSON数据
            data = response.json()
            return [Recipe.model_validate(recipe) for recipe in data]
    except Exception as error:
        print(f'获取远程菜谱数据失败: {error}')
        # 直接返回空列表，不尝试使用本地备份
        return []

# 获取所有分类
def get_all_categories(recipes: List[Recipe]) -> List[str]:
    categories = set()
    for recipe in recipes:
        if recipe.category:
            categories.add(recipe.category)
    return list(categories) 