import telebot
from telebot import types
import os

# 🔒 Твій токен — встав сюди між лапками ↓
BOT_TOKEN = os.getenv("8367504992:AAFzhcwo18OSq2AfrzGIvxJBSsWICBntutw")
bot = telebot.TeleBot(BOT_TOKEN)

# 🔸 Канал або група, куди надсилати анкети
CHANNEL_ID = "@clanapplications"  # або -100XXXXXXXXXXX якщо приватний канал

# 🔹 Текст правил
RULES_TEXT = """
❗ПРАВИЛА КЛАНА❗
• Энергия клана минимум 15к за сезон
• Участие в клановых съёмках для его продвижения (отказ только по уважительной причине)
• Мальчики КД - 5
• Девочки КД - 3
• Смена ника для приписки — срок неделя
• Участие в битве кланов

❕ПРАВИЛА ЧАТА❕
• Лидер — решающее слово: @HajimeDen
• Ответственная в отсутствие лидера: Леся @m_i_s_s_pubg
• Актив в чате (недельный неактив = БАН)
• Маты = мут 1 час

Уважение 🤝
Понимание 💬
Поддержка 💪
Помощь ❤️
🦔 ДОБРО ПОЖАЛОВАТЬ 🦔
"""

# ------------------ КОМАНДА /start ------------------
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Согласен с правилами", callback_data="agree")
    markup.add(btn)
    bot.send_message(message.chat.id, RULES_TEXT, reply_markup=markup)

# ------------------ СОГЛАСИЕ ------------------
@bot.callback_query_handler(func=lambda call: call.data == "agree")
def agree(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Отлично! 📝 Давай заполним анкету.\n\nВведи своё имя:")
    bot.register_next_step_handler(call.message, get_name)

# ------------------ АНКЕТА ------------------
def get_name(message):
    user_data = {"Имя": message.text}
    bot.send_message(message.chat.id, "📆 Укажи свой возраст:")
    bot.register_next_step_handler(message, get_age, user_data)

def get_age(message, user_data):
    user_data["Возраст"] = message.text
    bot.send_message(message.chat.id, "🌍 Из какой ты страны?")
    bot.register_next_step_handler(message, get_country, user_data)

def get_country(message, user_data):
    user_data["Страна"] = message.text
    bot.send_message(message.chat.id, "🏙️ Укажи свой город:")
    bot.register_next_step_handler(message, get_city, user_data)

def get_city(message, user_data):
    user_data["Город"] = message.text
    bot.send_message(message.chat.id, "📸 Отправь скрин игрового профиля:")
    bot.register_next_step_handler(message, get_profile, user_data)

def get_profile(message, user_data):
    if message.photo:
        user_data["Профиль"] = message.photo[-1].file_id
    else:
        user_data["Профиль"] = message.text
    bot.send_message(message.chat.id, "📊 Отправь скрин игровой статистики:")
    bot.register_next_step_handler(message, get_stats, user_data)

def get_stats(message, user_data):
    if message.photo:
        user_data["Статистика"] = message.photo[-1].file_id
    else:
        user_data["Статистика"] = message.text
    bot.send_message(message.chat.id, "🎖️ Звание в прошлом клане (если было):")
    bot.register_next_step_handler(message, get_rank, user_data)

def get_rank(message, user_data):
    user_data["Звание"] = message.text
    bot.send_message(message.chat.id, "🎮 В каком режиме чаще всего играешь?")
    bot.register_next_step_handler(message, get_mode, user_data)

def get_mode(message, user_data):
    user_data["Режим"] = message.text
    bot.send_message(message.chat.id, "💬 Чего ты ждёшь от нового клана?")
    bot.register_next_step_handler(message, get_expect, user_data)

def get_expect(message, user_data):
    user_data["Ожидания"] = message.text
    bot.send_message(message.chat.id, "⭐ Расскажи о своих особенностях:")
    bot.register_next_step_handler(message, finish_anketa, user_data)

def finish_anketa(message, user_data):
    user_data["Особенности"] = message.text

    text = (
        "📩 Новая анкета:\n\n"
        f"Имя: {user_data['Имя']}\n"
        f"Возраст: {user_data['Возраст']}\n"
        f"Страна: {user_data['Страна']}\n"
        f"Город: {user_data['Город']}\n"
        f"Звание: {user_data['Звание']}\n"
        f"Режим: {user_data['Режим']}\n"
        f"Ожидания: {user_data['Ожидания']}\n"
        f"Особенности: {user_data['Особенности']}"
    )

    bot.send_message(message.chat.id, "✅ Спасибо! Ваша анкета отправлена лидеру.")
    bot.send_message(CHANNEL_ID, text)

    # Отправляем фото, если были
    if isinstance(user_data.get("Профиль"), str) and user_data["Профиль"].startswith("Ag"):
        bot.send_photo(CHANNEL_ID, user_data["Профиль"], caption="📸 Игровой профиль")
    if isinstance(user_data.get("Статистика"), str) and user_data["Статистика"].startswith("Ag"):
        bot.send_photo(CHANNEL_ID, user_data["Статистика"], caption="📊 Игровая статистика")

# ------------------ ЗАПУСК ------------------
bot.polling(non_stop=True)
