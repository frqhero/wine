from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


def get_word(company_age):
    one = re.compile(r'^1$|.*[2-9]1$')
    to_five = re.compile(r'^[2-4]$|.*[023456789][2-4]$')
    if one.match(company_age):
        return 'год'
    elif to_five.match(company_age):
        return 'года'
    else:
        return 'лет'


def get_excel_data():
    excel_data_df = pandas.read_excel(
        'wine3.xlsx',
        sheet_name='Лист1',
        keep_default_na=False
    ).to_dict(orient='records')
    res = defaultdict(list)
    for excel_line in excel_data_df:
        category = excel_line['Категория']
        res[category].append(excel_line)
    return res


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    current_year = datetime.date.today().year
    company_age = str(current_year - 1920)
    word = get_word(company_age)
    company_string = f'{company_age} {word}'
    excel_data = get_excel_data()

    rendered_page = template.render(
        company_string=company_string,
        categories=excel_data
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
