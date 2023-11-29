from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot
from keyboards import reply
from googletrans import Translator


def to_user(message: Message, recipes_uri: list, recipes: list) -> None:
    """
    Отправляет пользователю информацию о рецептах.
    :param message: Объект сообщения от пользователя
    :param recipes_uri: Список URI рецептов
    :param recipes: Список рецептов
    """
    try:
        translator = Translator()
        for recipe in recipes:
            for find_uri in recipes_uri:
                if recipe.uri == find_uri:
                    label = translator.translate(recipe.label, dest='ru').text
                    bot.send_photo(chat_id=message.chat.id, photo=recipe.image)

                    # Отправка названия рецепта
                    bot.send_message(chat_id=message.chat.id, text=f"\nНазвание рецепта: {label}")

                    # Отправка списка ингредиентов
                    bot.send_message(chat_id=message.chat.id, text='\nИнгридиенты:')
                    [bot.send_message(chat_id=message.chat.id, text=f"\t{number + 1}. "
                            f"{translator.translate(ingredient.text, dest='ru').text}\n") for number, ingredient in
                            enumerate(recipe.ingredients)]

                    # Создание кнопки с ссылкой на рецепт
                    url_button = InlineKeyboardButton(text='Подробнее', url=recipe.url)
                    keyboard = InlineKeyboardMarkup([[url_button]])

                    # Отправка сообщения с кнопкой
                    bot.send_message(chat_id=message.chat.id, text='Ссылка на рецепт:', reply_markup=keyboard)

                    s_uri = recipe.uri.split('#')[1]
                    # Создание кнопки ссхранения рецепта
                    save_button = InlineKeyboardButton(text='Сохранить рецепт', callback_data=f'save:{s_uri}')
                    keyboard = InlineKeyboardMarkup([[save_button]])

                    # Отправка сообщения с кнопкой
                    bot.send_message(chat_id=message.chat.id, text=f'Добавить в список моих рецептов: {label}',
                                    reply_markup=keyboard)
    except Exception as err:
        print('Что то пошло не так:', err)
        bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так, попробуйте осуществить поиск с другим '
                                                       'названием рецепта или ингридиентами.')

        keyboard = reply.keyboards.create_main_keyboard()
        bot.send_message(message.chat.id, 'Выберите действие на клавиатуре:', reply_markup=keyboard)


def exact_or_alternative(message: Message, exact_matches: list, alternative_recipe: list, recipe: list) -> None:
    """
    Обработчик сообщения выбора точного совпадения или альтернативных рецептов.
    :param message: Объект сообщения от пользователя
    :param exact_matches: Список URI рецептов с точным совпадением
    :param alternative_recipe: Список URI альтернативных рецептов
    :param recipe: Список рецептов
    """
    try:
        if 'Точное совпадение' in message.text:
            keyboard = reply.keyboards.create_main_keyboard()
            bot.send_message(message.chat.id, 'Рецепты по запросу', reply_markup=keyboard)
            to_user(message, exact_matches, recipe)
        elif 'Альтернативные рецепты' in message.text:
            keyboard = reply.keyboards.create_main_keyboard()
            bot.send_message(message.chat.id, 'Рецепты по запросу', reply_markup=keyboard)
            to_user(message, alternative_recipe, recipe)
        elif message.text == 'Главное меню':
            keyboard = reply.keyboards.create_main_keyboard()
            bot.send_message(message.chat.id, 'Выберите действие на клавиатуре:', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Не корректный ввод, выберете действие на клавиатуре.')
            keyboard = reply.keyboards.create_main_keyboard()
            bot.send_message(message.chat.id, 'Выберите действие на клавиатуре:', reply_markup=keyboard)
    except Exception as err:
        print('Что-то пошло не так:', err)
        bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так')
