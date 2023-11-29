from telebot.types import Message
from loader import bot
from keyboards import reply
from handlers.custom_handlers import recipe_or_ingredients
from handlers.custom_handlers import history_favorites


@bot.message_handler(func=lambda message: message.text in ['Поиск рецепта', 'История запросов', 'Мои рецепты'])
def handle_message(message: Message) -> None:
    """
        Обработчик сообщений с кнопок клавиатуры.
        :param message: Объект сообщения от пользователя.
    """
    try:
        if message.text == 'Поиск рецепта':
            keyboard = reply.keyboards.create_recipe_or_ingredients_keyboard()
            bot.send_message(message.chat.id, 'Как будем искать по названию или ингридиентам?:', reply_markup=keyboard)
            bot.register_next_step_handler(message, recipe_or_ingredients.recipe_or_ingredients)
        elif message.text == 'История запросов':
            history_favorites.history_user(message)
        elif message.text == 'Мои рецепты':
            history_favorites.favorite_user(message)
    except Exception as e:
        # Обработка ошибок
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')
