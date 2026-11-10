import csv, openpyxl
w = openpyxl.load_workbook('city-lau-2021.xlsx', read_only=True, data_only=True)
s = w['CITY_LAU2021']
rows = s.iter_rows(values_only=True)
header = next(rows)
selected = [r for r in rows if r[2] == 'CH002C']
with open('city-lau-2021-CH002C.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f); writer.writerow(header); writer.writerows(selected)
print(len(selected))
