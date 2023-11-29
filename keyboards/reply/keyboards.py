from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    search_recipe_button = KeyboardButton('Поиск рецепта')
    history_button = KeyboardButton('История запросов')
    my_recipes_button = KeyboardButton('Мои рецепты')
    keyboard.add(search_recipe_button)
    keyboard.add(my_recipes_button, history_button)
    return keyboard


def create_search_recipe_keyboard(exact_matches, alternative_recipes):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    exact_matches_button = KeyboardButton(f'Точное совпадение ({exact_matches})')
    alternative_recipes_button = KeyboardButton(f'Альтернативные рецепты ({alternative_recipes})')
    start_menu_button = KeyboardButton('Главное меню')
    keyboard.add(exact_matches_button, alternative_recipes_button, start_menu_button)
    return keyboard


def create_recipe_or_ingredients_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    search_recipe_button = KeyboardButton('По названию рецепта')
    search_ingredients_button = KeyboardButton('По ингридиентам')
    back_button = KeyboardButton('Назад')
    keyboard.add(search_recipe_button, search_ingredients_button, back_button)
    return keyboard


def create_back_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = KeyboardButton('Назад')
    keyboard.add(back_button)
    return keyboard
