# GoogleAPI--psql-docker-and-telegram_bot

Ссылка на используемый Google Sheets документ:

https://docs.google.com/spreadsheets/d/1mqHm4fZe5gJeYUWynlpMQStfqajip6fQpxnyk7ApBi0/edit?usp=sharing 
(открыты права чтения и записи для пользователя irbispro10@gmail.com) 

Инструкция по запуску разработанных скриптов на языке Python 3.
п.1, п.2, п.3 описания проекта:
	Клонировать проект 
	
	Папка
	/GoogleAPI_suppliesSheet-postgres and telegram-bot

	Установка зависимостей
	python -m pip install -r requirements.txt

	Запустить скрипт, предварительно установив настройки БД в начале скрипта (# configs (вводим свои настройки) HOST, PORT, USER, PASSWORD, DB)
	postgresql_connection.py
	
	*!Вне ТЗ, но удобно для работы сразу отражать рассчетный столбец в GoogleSheets. Для этого запустить
	sup_data_process.py

п.4.а.:
	Папка
	/Docker_GoogleAPI_suppliesSheet
	
	Из указанной директории поднимаем
	docker-compose up --build
	
	Чтобы поднять конкретный контейнер заходим в папку где лежит его Dockerfile, наприимер /app/Dockerfile
	docker build -t new_image_name .

п.4.b:
	Папка
	/GoogleAPI_suppliesSheet-postgres and telegram-bot

	Запустить скрипт, предварительно установив Ваш telegram user ID, который выдает @getmyid_bot (в скрипте изменить значение YOUR_USER_ID)
	sup_terms_bot.py


Описание проекта:

1. Получение данных с документа при помощи Google API, сделанного в [Google Sheets]
(https://docs.google.com/spreadsheets/d/1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g/edit) (копируются в свой Google аккаунт и выдаются самому себе права).
2. Данные добавляются в БД, в том же виде, что и в файле–источнике, с добавлением колонки «стоимость в руб.»  
    a. СУБД на основе PostgreSQL.
    b. Данные для перевода $ в рубли по курсу [ЦБ РФ](https://www.cbr.ru/development/SXML/).  
3. Скрипт работает постоянно для обеспечения обновления данных в онлайн режиме (строки в ИСХОДНОЙ Google Sheets таблице могут удаляться, добавляться и изменяться).
4. a. Упаковка решения в docker контейнер  
   b. Функционал проверки соблюдения «срока поставки» из таблицы. В случае, если срок прошел, скрипт отправляет уведомление в Telegram.