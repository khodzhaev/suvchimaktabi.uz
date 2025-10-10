
from control.models import Student, District, Region
from datetime import datetime
import part_3 as part_1

import time

for i in part_1.arr:
    print(i)
    try:
        s = Student.objects.get(phone=part_1.arr[i]['Номер телефона'])
    except: pass
    try:
        district = str(part_1.arr[i]['Регион']).replace("ʻ", "'")
        d = District.objects.get(title=district)
        s.district = d
    except: pass
    try:
        region = str(part_1.arr[i]['Район']).replace("ʻ", "'")
        r = Region.objects.get(title=region)
        s.region = r
    except: pass
    try:
        date_str = part_1.arr[i]['Дата регистрации']
        date_obj = datetime.strptime(date_str, '%m/%d/%Y, %I:%M:%S %p')
        s.date_created = date_obj
    except: pass
    try:
        s.save()
    except: pass
    time.sleep(0.1)
