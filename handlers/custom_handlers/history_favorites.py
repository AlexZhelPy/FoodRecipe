from database import database
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from handlers.custom_handlers import recipe_to_user
from api.food_api import food_con
from loader import bot
import json


def history_user(message: Message):
    user = database.get_user(message.from_user.id)
    history_list = json.loads(user[3])
    for number, element_history in enumerate(history_list):
        bot.send_message(message.chat.id, f'{number + 1}. {element_history}')


def favorite_user(message: Message):
    user = database.get_user(message.from_user.id)
    favorite_list = json.loads(user[4])
    for number, element_favorite in enumerate(favorite_list):
        label_uri = element_favorite.split(',')
        keyboard = InlineKeyboardMarkup(row_width=2)
        open_button = InlineKeyboardButton("Открыть рецепт", callback_data=f"open:{label_uri[1]}")
        delete_button = InlineKeyboardButton("Удалить рецепт", callback_data=f"delete:{label_uri[1]}")

        keyboard.add(open_button, delete_button)

        bot.send_message(message.chat.id, f'{number + 1}. {label_uri[0]}', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('save:'))
def save_recipe_handler(call):
    recipe_uri = call.data.split(':')[1]
    label_text = call.message.text.split(': ')[1]
    uri_label = label_text + ',' + recipe_uri
    message = call.message.chat
    database.insert_user(message.id, message.first_name,
                         message.last_name, None, uri_label)
    bot.answer_callback_query(call.id, text='Рецепт сохранен')


@bot.callback_query_handler(func=lambda call: call.data.startswith('open:'))
def open_recipe_handler(call):
    recipe_uri = call.data.split(':')[1]
    recipe_search = food_con.RecipeSearch(parameters={})

    result_recipe = []
    result_uri = []
    recipe = recipe_search.get_recipe_by_uri('http://www.edamam.com/ontologies/edamam.owl#' + recipe_uri)
    result_recipe.append(recipe)
    result_uri.append('http://www.edamam.com/ontologies/edamam.owl#' + recipe_uri)
    if recipe is not None:
        recipe_to_user.to_user(call.message, result_uri, result_recipe)
    else:
        print("Recipe not found")


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete:'))
def delete_recipe_handler(call):
    element_name = call.data.split(':')[1]
    user = database.get_user(call.message.chat.id)
    favorite_list = json.loads(user[4])

    for i, element in enumerate(favorite_list):
        if element_name in element:
            favorite_list.pop(i)
            new_list = json.dumps(favorite_list)
            database.update_favorite_user(user[0], new_list)

            bot.answer_callback_query(call.id, text='Рецепт удален')
            break

    else:
        bot.answer_callback_query(call.id, text='Рецепт не найден')
