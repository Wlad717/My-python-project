import pandas as pd
import requests
import csv
from lxml import etree


currency_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
required_currency = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']


def get_info(tree, one_currency):
    required_information = tree.xpath(f"//Valute[CharCode='{one_currency}']")
    if not required_information:
        return None
    currency_vunit = float(required_information[0].find('VunitRate').text.replace(',', '.'))
    return currency_vunit


def prepare_currency_information(date):
    response = requests.get(f'{currency_URL}?date_req={date.strftime("%d/%m/%Y")}')
    current_tree = etree.fromstring(response.content)
    current_row = [date.strftime('%Y-%m')]

    for one_currency in required_currency:
        current_row.append(get_info(current_tree, one_currency))
    return current_row


def main():
    start_date = pd.to_datetime('2003.01.01')
    end_date = pd.to_datetime('2024.12.01')
    date_offset = pd.DateOffset(months=1)
    current_date = start_date

    with open('csv_prepared_files/currency_values.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['date'] + required_currency)
        while current_date <= end_date:
            row = prepare_currency_information(current_date)
            writer.writerow(row)
            current_date += date_offset


if __name__ == "__main__":
    main()