from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import re
import pandas

env = Environment(loader=FileSystemLoader('.'),
                  autoescape=select_autoescape(['html', 'xml']))

template = env.get_template('template.html')

current_year = datetime.date.today().year
company_age = str(current_year - 1920)
one = re.compile(r'^1$|.*[2-9]1$')
to_five = re.compile(r'^[2-4]$|.*[023456789][2-4]$')
more_then_hund = re.compile(r'1[1-3]$')
if one.match(company_age):
    word = 'год'
elif to_five.match(company_age):
    word = 'года'
else:
    word = 'лет'

company_string = f'{company_age} {word}'
excel_data_df = pandas.read_excel('wine.xlsx', sheet_name='Лист1')

rendered_page = template.render(
    company_string=company_string,
    excel_data=excel_data_df.to_dict(orient='records')
    )

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
