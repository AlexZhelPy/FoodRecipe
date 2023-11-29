from telebot.types import Message
from loader import bot
from keyboards import reply
from handlers.custom_handlers import process_recipe_message


def recipe_or_ingredients(message: Message) -> None:
    """
    Обработчик сообщения выбора поиска.
    :param message: Объект сообщения от пользователя
    """
    try:
        if message.text == 'По названию рецепта':
            bot.send_message(message.chat.id, 'Введите название рецепта.')
            keyboard = reply.keyboards.create_back_keyboard()
            bot.send_message(message.chat.id, 'Или нажмите кнопку "Назад" для выхода в главное меню.',
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, process_recipe_message.process_recipe_message,
                                           ingredients=False)
        elif message.text == 'По ингридиентам':
            bot.send_message(message.chat.id, 'Введите ингридиенты через запятую.')
            keyboard = reply.keyboards.create_back_keyboard()
            bot.send_message(message.chat.id, 'Или нажмите кнопку "Назад" для выхода в главное меню.',
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, process_recipe_message.process_recipe_message,
                                           ingredients=True)
        elif message.text == 'Назад':
            keyboard = reply.keyboards.create_main_keyboard()
            bot.send_message(message.chat.id, 'Выберите действие на клавиатуре.', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Не корректный ввод, выберете действие на клавиатуре.')
            bot.send_message(message.chat.id, 'Как будем искать по названию или ингридиентам?')
            bot.register_next_step_handler(message, recipe_or_ingredients)
    except Exception as e:
        # Обработка ошибок
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')
