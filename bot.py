import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Токен вашего бота
API_TOKEN = '7516502805:AAFzJahj1y0tdJTs9vJNOZ0gKEwZ8z2Hli0'

# Настройка клиента Telegram
bot = telebot.TeleBot(API_TOKEN)

# Настройка доступа к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds/google_sheets_credentials.json', scope)  # Обновите путь здесь
client = gspread.authorize(creds)

# Открываем таблицу
try:
    sheet = client.open("Цитадель сплетен МИРЭА").sheet1
except gspread.SpreadsheetNotFound:
    print("Ошибка: Таблица 'Цитадель сплетен МИРЭА' не найдена. Убедитесь, что таблица существует и что у вас есть к ней доступ.")
    exit(1)

# Обработчик сообщений
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправьте мне сплетни, и я добавлю их в таблицу.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Записываем сообщение в таблицу
        sheet.append_row([message.from_user.username, message.text])
        bot.reply_to(message, "Сплетня добавлена в таблицу!")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при добавлении сплетни.")
        print(f"Ошибка: {e}")

# Запуск бота
bot.polling()
