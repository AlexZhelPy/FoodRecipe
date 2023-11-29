from telebot.types import Message

from loader import bot
from keyboards import reply


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(
        message, "Не корректный ввод!!!"
    )
    keyboard = reply.keyboards.create_main_keyboard()
    bot.send_message(message.chat.id, 'Выберите действие на клавиатуре:', reply_markup=keyboard)
