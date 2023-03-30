import pandas
from pprint import pprint

excel_data_df = pandas.read_excel(
    'wine2.xlsx', 
    sheet_name='Лист1',
    keep_default_na=False).to_dict(orient='records')
res = {}
for excel_line in excel_data_df:
    category = excel_line['Категория']
    curr_list = res.get(category, [])
    curr_list.append(excel_line)
    res[category] = curr_list

pprint(res)
