from telebot.types import Message
from loader import bot
from keyboards import reply
from api.food_api import recipe_processing, food_con
from handlers.custom_handlers import recipe_to_user
from langdetect import detect
from googletrans import Translator
from database import database


def process_recipe_message(message: Message, ingredients: bool) -> None:
    """
        Обработчик сообщения с названием рецепта.
        :param ingredients: Флаг, осуществление поиска по названию или ингридиентам.
        :param message: Объект сообщения от пользователя.
    """
    try:
        if message.text == 'Назад':
            keyboard = reply.keyboards.create_main_keyboard()
            bot.send_message(message.chat.id, 'Выберите действие на клавиатуре.', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Поиск рецептов...')
            recipe_name = message.text
            database.insert_user(message.from_user.id, message.from_user.first_name,
                                 message.from_user.last_name, recipe_name)
            translator = Translator()
            if detect(recipe_name) != 'en':
                recipe_name = translator.translate(recipe_name, dest='en').text
            recipe = food_con.RecipeSearch({'q': recipe_name, 'to': 5}).get_results()
            if recipe:
                exact_matches = recipe_processing.get_exact_matches(recipe, recipe_name, ingredients)
                alternative_recipes = recipe_processing.get_alternative_recipes(recipe, recipe_name)

                keyboard = reply.keyboards.create_search_recipe_keyboard(len(exact_matches), len(alternative_recipes))
                bot.send_message(message.chat.id, 'Показать рецепты по точному совпадению запроса или альтернативные '
                                                  'варианты?:', reply_markup=keyboard)
                bot.register_next_step_handler(message, recipe_to_user.exact_or_alternative, exact_matches,
                                               alternative_recipes, recipe)
            else:
                raise ValueError('Рецепт не найден')

    except Exception as err:
        # Обработка ошибок
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(err)}')
