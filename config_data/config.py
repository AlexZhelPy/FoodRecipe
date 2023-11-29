import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env!")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
API_FOOD_ID = os.getenv("API_FOOD_ID")
API_FOOD_KEY = os.getenv("API_FOOD_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку")
)
