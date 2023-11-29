from telebot.types import Message
from loader import bot
from database import database
from keyboards import reply


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    database.create_table()
    user = database.get_user(message.from_user.id)
    if not user:
        database.insert_user(message.from_user.id, message.from_user.first_name,
                             message.from_user.last_name)
        bot.reply_to(message, 'Приветствую вас на FoodRecipe.')

    keyboard = reply.keyboards.create_main_keyboard()
    bot.send_message(message.chat.id, 'Выберите действие на клавиатуре:', reply_markup=keyboard)
