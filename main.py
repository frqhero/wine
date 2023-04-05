from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import os
import re

from dotenv import load_dotenv
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


def get_wine_entries(source_table_path):
    wines = pandas.read_excel(
        source_table_path,
        sheet_name='Лист1',
        keep_default_na=False
    ).to_dict(orient='records')
    categories = defaultdict(list)
    for excel_line in wines:
        category = excel_line['Категория']
        categories[category].append(excel_line)
    return categories


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    current_year = datetime.date.today().year
    foundation_date = 1920
    company_age = str(current_year - foundation_date)
    word = get_word(company_age)
    company_age_string = f'{company_age} {word}'

    source_table_path = os.getenv('source_table_path')
    wine_entries = get_wine_entries(source_table_path)

    rendered_page = template.render(
        company_age_string=company_age_string,
        wine_entries=wine_entries
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    load_dotenv()
    main()
