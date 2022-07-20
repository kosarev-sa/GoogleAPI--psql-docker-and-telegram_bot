import requests as rq
import datetime as dt
from decimal import Decimal

# Получаем строку информации с котировками с сайта Банка России
# (по состоянию на последнюю зарегистрированную дату)
def cbr_get_content():
    responce = rq.get("http://www.cbr.ru/scripts/XML_daily.asp")
    encodings = rq.utils.get_encoding_from_headers(responce.headers)
    content = responce.content.decode(encoding=encodings)
    return content

# Функция получения точного значения курса заданной валюты к рублю
def currency_rate(info, currency):
    input_currency = currency.upper()
    code = info.find(input_currency)
    if code == -1:
        return None
    code_value = info.find(",", code)
    text = info[code_value - 3:code_value + 5].replace(",", ".")
    value = ""
    for symbol in text:
        if symbol.isdigit() or symbol == ".":
            value += symbol
    rate = Decimal(value)
    rate = rate.quantize(Decimal("1.0000"))
    return rate

# Функция получения даты опубликования курса
def get_date(info):
    code_date = info.find('Date="')
    content_date = (info[code_date+6:code_date+16].split("."))
    d, m, y = map(int, content_date)
    date = dt.date(y, m, d)
    return date


if __name__ == '__main__':
    cur = "USD"
    responce = cbr_get_content()
    result = currency_rate(responce, cur)
    date = get_date(responce)

    if result is None:
        print(result)
    else:
        print(f"{cur}/RUB: {result}, {date}")
