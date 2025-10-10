


import part_3 as part_1
import time


def xxx():
    from control.models import Student, Region, District
    for i in part_1.arr:
        time.sleep(0.1)
        print(part_1.arr[i]['Номер сертификата'])
        try:
            region = Region.objects.get(title=part_1.arr[i]['Район'])
        except:
            region = None
        try:
            if part_1.arr[i]['Регион'] != "":
                district, created = District.objects.get_or_create(title=part_1.arr[i]['Регион'])
                if created:
                    district.region = region
                    district.save()
            else:
                district = None
        except:
            district = None
        if part_1.arr[i]['Пол'] == 'Еркак':
            tgender = 'male'
        else:
            tgender = 'female'
        if part_1.arr[i]['Статус сертификата'] == 'Рўйхатдан ўтмоқда':
            tstatus = 'start'
        else:
            tstatus = 'end'
        Student.objects.create(
            region = region,
            district = district,
            fio = part_1.arr[i]['ФИО'],
            phone = part_1.arr[i]['Номер телефона'],
            birthday = part_1.arr[i]['Дата рождения'],
            gender = part_1.arr[i]['Пол'],
            company = part_1.arr[i]['Организация'],
            activity = part_1.arr[i]['Сфера деятельности'],
            job = part_1.arr[i]['Должность'],
            date_created = part_1.arr[i]['Дата регистрации'],
            platform = part_1.arr[i]['Платформа'],
            status = part_1.arr[i]['Статус сертификата'],
            certificate_id = part_1.arr[i]['Номер сертификата'],
            tgender = tgender,
            tstatus = tstatus
        )
        
