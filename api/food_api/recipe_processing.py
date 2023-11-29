from typing import List
from api.food_api.food_con import Recipe


def get_exact_matches(recipes: List['Recipe'], query: str, ingredients: bool) -> List[str]:
    """Получение точного совпадения по названию рецепта или ингридиентов

        Аргументы:
            recipes (List[Recipe]): Список рецептов
            query (str): Запрос пользователя
            ingredients (bool): Флаг для выбора совпадения по названию или ингридиентам

        Возвращает:
            List[str]: Лист с URI рецептов
        """
    try:
        exact_matches = []
        for recipe in recipes:
            if ingredients:
                query_space = query.replace(' ', '')
                query_list = list(query_space.split(','))
                if len(query_list) == len(recipe.ingredients) and all(
                        find_ingredient in line.text for line, find_ingredient in zip(recipe.ingredients, query_list)):
                    exact_matches.append(recipe.uri)
            else:
                if query.lower() == recipe.label.lower():
                    exact_matches.append(recipe.uri)
        return exact_matches
    except Exception as err:
        print(f"Ошибка при получении точных совпадений: {err}")
        return []


def get_alternative_recipes(recipes: List["Recipe"], query: str) -> List[str]:
    """Получение альтернативных рецептов по названию или ингридиентам

            Аргументы:
                recipes (List[Recipe]): Список рецептов
                query (str): Запрос пользователя

            Возвращает:
                List[str]: Лист с URI рецептов
            """
    try:
        alternative_recipes = []
        for recipe in recipes:
            if query.lower() != recipe.label.lower():
                alternative_recipes.append(recipe.uri)
        return alternative_recipes
    except Exception as e:
        print(f"Ошибка при получении альтернативных рецептов: {e}")
        return []
