import requests
import datetime
import time
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Настройка бота Telegram
token = 'ТОКЕН'
updater = Updater(token=token)
dispatcher = updater.dispatcher

# Настройка OpenWeather
api_key = 'ВАШ_API_КЛЮЧ'
base_url_weather = 'http://api.openweathermap.org/data/2.5/weather'

# Настройка MoonAPI
base_url_moon = 'https://api.moondaily.org/api/v2/moon-phase'
api_token = 'ВАШ_API_ТОКЕН'

# Словарь с соответствием кодов стран и флагов
country_codes = {
    'ru': '🇷🇺',
    'ua': '🇺🇦',
    'by': '🇧🇾',
    'kz': '🇰🇿',
    'us': '🇺🇸',
    'gb': '🇬🇧',
    'de': '🇩🇪',
    'fr': '🇫🇷',
    'es': '🇪🇸',
    'it': '🇮🇹',
}

# Словарь с соответствием кодов языков и языков
language_codes = {
    'ru': 'Русский',
    'en': 'Английский',
    'uk': 'Украинский',
    'be': 'Белорусский',
    'kk': 'Казахский',
}

# Список мотивирующих сообщений
motivational_messages = [
    'Не бойся неудач. Они лишь ступеньки к успеху.',
    'Даже самая дальняя дорога начинается с первого шага.',
    'Успех – это не окончательная точка, неудача – не фатальный конец. Важно мужество продолжать.',
    'Невозможно – это всего лишь громкое слово, за которым прячутся маленькие люди. Им проще жить в привычном мире, чем найти в себе силы что-то изменить.',
    'Препятствия – это те страшные вещи, которые вы видите, когда отводите взгляд от цели.',
    'Падая, смотри не упади духом.',
    'Единственный человек, который может остановить вас – это вы сами.',
    'Побеждает тот, кто не сдается.',
    'Мы не можем контролировать ветер, но можем расправить паруса.',
    'Если ты можешь мечтать об этом, ты можешь это сделать.',
]


# Функция для получения времени суток
def get_time_of_day():
    hour = datetime.datetime.now().hour
    if hour < 6:
        return 'ночь'
    elif 6 <= hour < 12:
        return 'утро'
    elif 12 <= hour < 18:
        return 'день'
    else:
        return 'вечер'


# Функция для приветствия пользователя
def greet_user(update, context):
    time_of_day = get_time_of_day()
    greetings = {
        'ночь': 'Доброй ночи',
        'утро': 'Доброе утро',
        'день': 'Добрый день',
        'вечер': 'Добрый вечер',
    }
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'{greetings[time_of_day]}, {update.effective_chat.first_name}!')


# Функция для получения погоды
def get_weather(update, context):
    city = update.message.text
    language_code = update.effective_chat.language_code
    params = {'q': city, 'appid': api_key, 'units': 'metric', 'lang': language_code}
    response = requests.get(base_url_weather, params=params)
    data = response.json()

    if 'cod' in data and data['cod'] == '404':
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Город {city} не найден.')
        return

    country_code = data['sys']['country'].lower()
    weather = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    output = (
        f'Погода в {city} ({country_codes.get(country_code, "")} на {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}:\n'
        f'Погода: {weather}\n'
        f'Температура: {temperature}°C\n'
        f'Влажность: {humidity}%\n'
        f'Скорость ветра: {wind_speed} м/с')

    context.bot.send_message(chat_id=update.effective_chat.id, text=output)


# Функция для получения фазы луны
def get_moon_phase(update, context):
    params = {'api_key': api_token, 'date': datetime.datetime.now().strftime("%Y-%m-%d")}
    response = requests.get(base_url_moon, params=params)
    data = response.json()

    phase = data['phase']
    illumination = data['illumination']

    output= (f'Фаза луны на {datetime.datetime.now().strftime("%d.%m.%Y")}:\n'
               f'Фаза: {phase}\n'
               f'Освещенность: {illumination}%')

    context.bot.send_message(chat_id=update.effective_chat.id, text=output)

# Функция для отображения списка стран для выбора
def show_country_list(update, context):
    country_list = '\n'.join([f'{country_code.upper()} - {country_name}' for country_code, country_name in country_codes.items()])
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Список доступных стран:\n{country_list}')

# Функция для отображения списка языков для выбора
def show_language_list(update, context):
    language_list = '\n'.join([f'{language_code.upper()} - {language_name}' for language_code, language_name in language_codes.items()])
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Список доступных языков:\n{language_list}')

# Функция для обработки информации о поле и возрасте пользователя
def get_user_info(update, context):
    gender = update.message.text
    if gender not in ['мужской', 'женский']:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Пожалуйста, укажите корректный пол (мужской или женский).')
        return

    age = update.message.text
    if not age.isdigit() or int(age) < 0 or int(age) > 120:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Пожалуйста, укажите корректный возраст (от 0 до 120 лет).')
        return

    context.bot.send_message(chat_id=update.effective_chat.id, text='Отлично! Теперь я знаю немного больше о вас.')

    # Предложить пользователю добавиться в группу
    group_link = 'ссылка_на_группу'
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Хотите присоединиться к нашей группе? Ссылка на группу: {group_link}')

# Обработка команд
dispatcher.add_handler(CommandHandler('weather', get_weather))
dispatcher.add_handler(CommandHandler('moon', get_moon_phase))
dispatcher.add_handler(CommandHandler('countries', show_country_list))
dispatcher.add_handler(CommandHandler('languages', show_language_list))

# Обработка сообщений
dispatcher.add_handler(MessageHandler(Filters.text, greet_user))
dispatcher.add_handler(MessageHandler(Filters.regex('(мужской)|(женский)'), get_user_info))

# Запуск бота
updater.start_polling()

# Остановка бота (при нажатии Ctrl+C)
updater.idle()