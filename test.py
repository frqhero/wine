from pprint import pprint
from collections import defaultdict

import pandas


excel_data_df = pandas.read_excel(
    'wine3.xlsx',
    sheet_name='Лист1',
    keep_default_na=False
    ).to_dict(orient='records')
res = defaultdict(list)
for excel_line in excel_data_df:
    category = excel_line['Категория']
    res[category].append(excel_line)

pprint(res)
