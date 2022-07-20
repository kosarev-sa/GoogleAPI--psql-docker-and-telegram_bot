'''Скрипт работы с Google API'''
import os.path

from googleapiclient.discovery import build
from google.oauth2 import service_account

from cbr_rate_rub import cbr_get_content, currency_rate

# Формируем параметры для входа (перечень сервисов и путь к файлу разрешений с Google API)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# ID электронной таблицы и название листа
SAMPLE_SPREADSHEET_ID = '1mqHm4fZe5gJeYUWynlpMQStfqajip6fQpxnyk7ApBi0'
SAMPLE_RANGE_NAME = 'Лист1'

# Собираем клиентский сервис для извлечения значений из электронной таблицы
service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()


def main(currency='USD'):
    # Получаем данные, в т.ч. значения Sheets API
    result = service.get(majorDimension='ROWS', spreadsheetId=SAMPLE_SPREADSHEET_ID,
                         range=SAMPLE_RANGE_NAME).execute()
    data_from_sheet_rows = result.get('values', [])

    # Получаем текущий курс валюты с сайта Банка России
    cbr_rates_info = cbr_get_content()
    rate = currency_rate(cbr_rates_info, currency)

    # Рассчитываем стоимость в рублях и формируем словарь со значениями рассчетного столбца
    data_to_add = {'values': [['стоимость в руб.']]}
    for item in data_from_sheet_rows[1:]:  # проходим по столбцу со стоимостью в долларах
        rub_cost = float(item[2]) * float(rate)
        row_data = [f'{rub_cost:.2f}']
        data_to_add['values'].append(row_data)

    # Собираем данные для INSERT'а в базу данных, в т.ч. рассчетный столбец
    data_to_psql = []
    for row in data_from_sheet_rows[1:]:
        # добавляем исходные данные
        row_to_psql = row[:4]
        # добавляем рассчетные данные по соответствующему индексу строки
        row_to_psql.append(data_to_add['values'][data_from_sheet_rows.index(row)][0])
        data_to_psql.append(tuple(row_to_psql))
    return data_to_psql


if __name__ == '__main__':
    # !Вне ТЗ, но удобно для работы сразу отражать рассчетный столбец в GoogleSheets:
    # Определяем лист и диапазон (А1-нотацию) для обновления/добавления данных в GoogleSheets
    START_RANGE = 'E1'
    END_RANGE = f'E{len(main())+1}'
    range_ = f'{SAMPLE_RANGE_NAME}!{START_RANGE}:{END_RANGE}'
    # C помощью listcomprehensions формируем нужный формат данных
    data_to_add = {'values': [[tpl[-1]] for tpl in main()]}
    data_to_add['values'].insert(0, ['стоимость в руб.'])
    # Обновляем таблицу (добавляем данные в рассчетный столбец 'E')
    request = service.update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                             range=range_,
                             valueInputOption='RAW',
                             body=data_to_add)
    request.execute()
