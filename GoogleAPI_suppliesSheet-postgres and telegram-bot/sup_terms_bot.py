import time
from datetime import datetime
import telebot

from sup_data_process import main

# Токен, который выдает @BotFather (здесь токен бота @sup_terms_bot)
bot = telebot.TeleBot('5594971914:AAEG9d2S74mG9OgMXgeDy091c4cntkQXJSg')
# Ваш telegram user ID, который выдает @getmyid_bot
YOUR_USER_ID = '1684251847'

# Интервал между проверками изменений, сек.
interval = 60

checked = []
while True:
    # Загружаем последние данные
    data = main()
    # Проверяем сроки и запоминаем проверенные данные
    for supply in data:
        # Если срок поставки вышел и ещё не уведомляли, то уведомляем
        if datetime.strptime(supply[3], '%d.%m.%Y').date() < datetime.now().date() \
                and supply not in checked:
            message = f'Cрок поставки заказа №{supply[2]} вышел {supply[3]}! ' \
                      f'\nCтоимость {supply[4]}$'
            bot.send_message(YOUR_USER_ID, message)
            checked.append(supply)
    # Ждём заданный интервал времени перед следующей проверкой
    time.sleep(interval)
