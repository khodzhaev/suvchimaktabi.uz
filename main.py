

import openpyxl

# Открываем файл XLSX
workbook = openpyxl.load_workbook('./suvchilar-maktabi.xlsx')

# Получаем первый лист
sheet = workbook.active

# Создаем пустой словарь для хранения данных
data_dict = {}

# Проходимся по строкам и столбцам и заполняем словарь
for row_index, row in enumerate(sheet.iter_rows(min_row=2), start=2):
    item_dict = {
        'ФИО': row[0].value,
        'Пол': row[1].value,
        'Дата рождения': row[2].value,
        'Организация': row[3].value,
        'Номер телефона': row[4].value,
        'Сфера деятельности': row[5].value,
        'Должность': row[6].value,
        'Район': row[7].value,
        'Регион': row[8].value,
        'Платформа': row[9].value,
        'Дата регистрации': row[10].value,
        'Статус сертификата': row[11].value,
        'Номер сертификата': row[12].value,
    }
    data_dict[row_index] = item_dict


with open('file.py', 'w') as f:
    f.write(str(data_dict))