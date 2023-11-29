from requests import get
from config_data.config import API_FOOD_ID, API_FOOD_KEY
from typing import List, Optional


class RecipeSearch:
    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters
        self.parameters["app_id"] = API_FOOD_ID
        self.parameters["app_key"] = API_FOOD_KEY
        self._request = None
        self.basePath = "https://api.edamam.com/search"

    def get_results(self) -> List["Recipe"]:
        """Получение результатов поиска рецептов

        Возвращает:
            Recipe[]: Список рецептов"""
        try:
            self._request = get(self.basePath, params=self.parameters)
            self._request.raise_for_status()  # Проверка на ошибки HTTP
            hits = self._request.json()["hits"]
            result = []
            for hit in hits:
                result.append(Recipe(hit["recipe"]))
            return result
        except Exception as err:
            print(f"Ошибка при получении результатов поиска: {err}")
            return []

    def get_recipe_by_uri(self, uri: str) -> Optional["Recipe"]:
        """Получение рецепта по URI

        Аргументы:
            uri (str): URI рецепта

        Возвращает:
            Recipe: Рецепт или None, если рецепт не найден"""
        try:
            self.parameters["r"] = uri
            self._request = get(self.basePath, params=self.parameters)
            self._request.raise_for_status()  # Проверка на ошибки HTTP
            recipe_data = self._request.json()[0]
            recipe = Recipe(recipe_data)
            return recipe
        except requests.exceptions.RequestException as err:
            print(f"Error retrieving recipe: {err}")
            return None


class Recipe:
    def __init__(self, source: Optional[dict] = None) -> None:
        if source is not None:
            self.uri: Optional[str] = source.get("uri") or None
            self.label: Optional[str] = source.get("label") or None
            self.image: Optional[str] = source.get("image") or None
            self.url: Optional[str] = source.get("url") or None
            self.calories: Optional[float] = source.get("calories") or None
            self.ingredients: List[Ingredient] = [Ingredient(x) for x in source.get("ingredients", [])]
        else:
            self.uri = None
            self.label = None
            self.image = None
            self.url = None
            self.calories = None
            self.ingredients = None


class Ingredient:
    def __init__(self, source: Optional[dict] = None) -> None:
        if source is not None:
            self.text: Optional[str] = source.get("text") or None
            self.weight: Optional[float] = source.get("weight") or None
        else:
            self.text = None
            self.weight = None
