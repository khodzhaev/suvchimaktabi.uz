import dramatiq
from django.core.mail import send_mail
import cv2
from fpdf import FPDF
from pathlib import Path
from control.models import Student, Excel, District, FA
from django.conf import settings
from eskiz_sms import EskizSMS
from openpyxl import Workbook
import numpy as np
import qrcode
import random
import os

BASE_DIR = Path(__file__).resolve().parent.parent


@dramatiq.actor
def send_sms_code(phone, code):
    message = f"suvchimaktabi.uz parolni tiklash uchun maxfiy kod: {code}"
    eskiz = EskizSMS(email=settings.ESKIZ_LOGIN, password=settings.ESKIZ_PASSWORD)
    a = eskiz.send_sms(phone, message, from_whom='4546', callback_url=None)


@dramatiq.actor
def send_sms_notification(phone, code):
    message = f'Tabriklaymiz! Siz "Fermer va agroklasterlar" o\'quv kursidan muvaffaqiyatli ro\'yxatdan o\'tdingiz. Kurs yakunida sizga sertifikat va esdalik sovg\'alar taqdim etiladi.'
    eskiz = EskizSMS(email=settings.ESKIZ_LOGIN, password=settings.ESKIZ_PASSWORD)
    a = eskiz.send_sms(phone, message, from_whom='4546', callback_url=None)



def generate_qr_code(data):
    # Создание объекта QR кода с настройками для удаления внешнего отступа
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=0  # Установка границы в 0 для удаления внешнего отступа
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Создание изображения QR-кода
    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Преобразование изображения PIL в массив NumPy для использования с OpenCV
    img_qr = np.array(img_qr)
    img_qr = cv2.cvtColor(img_qr, cv2.COLOR_RGB2BGR)
    
    return img_qr

def add_qr_code_to_image(image, qr_code, position=(0, 0)):
    x, y = position
    qr_height, qr_width = qr_code.shape[:2]
    image[y:y+qr_height, x:x+qr_width] = qr_code




@dramatiq.actor
def generate_pdf(certificate_id):

    person = Student.objects.get(certificate_id=certificate_id)

    try:
        os.remove(BASE_DIR / f'media/certificate/{person.certificate_id}.jpg')
    except:
        pass

    if person.fio == None or len(person.fio) == 0:
        person.fio = 'Ism kiritilmagan'
        person.save()

    template = cv2.imread(str(BASE_DIR / 'media/template.jpg'))

    if  person.fio[0].lower() in 'йцукенгшщзфывапролдячсмитьбюзхжэъ':
        full_name = ""

        for B in person.fio.lower():
            if B=='а':full_name+='a'
            elif B=='б':full_name+='b'
            elif B=='в':full_name+='v'
            elif B=='г':full_name+='g'
            elif B=='д':full_name+='d'
            elif B=='е':full_name+='e'
            elif B=='ё':full_name+='yo'
            elif B=='ж':full_name+='j'
            elif B=='з':full_name+='z'
            elif B=='и':full_name+='i'
            elif B=='й':full_name+='y'
            elif B=='к':full_name+='k'
            elif B=='л':full_name+='l'
            elif B=='м':full_name+='m'
            elif B=='н':full_name+='n'
            elif B=='о':full_name+='o'
            elif B=='п':full_name+='p'
            elif B=='р':full_name+='r'
            elif B=='с':full_name+='s'
            elif B=='т':full_name+='t'
            elif B=='у':full_name+='u'
            elif B=='ф':full_name+='f'
            elif B=='х':full_name+='x'
            elif B=='ч':full_name+='ch'
            elif B=='ц':full_name+='ts'
            elif B=='ш':full_name+='sh'
            elif B=='щ':full_name+='sh'
            elif B=='ь':full_name+=''
            elif B=='ы':full_name+=''
            elif B=='ъ':full_name+="'"
            elif B=='э':full_name+='e'
            elif B=='ю':full_name+='yu'
            elif B=='я':full_name+='ya'
            elif B=='ғ':full_name+="g'"
            elif B=='қ':full_name+='q'
            elif B=='ў':full_name+="o'"
            elif B=='ҳ':full_name+='h'
            elif B==' ':full_name+=' '
            else: full_name+=''

        full_name = full_name.title()

    else: full_name = person.fio

    if len(full_name) <= 10: x_dot = 480
    elif len(full_name) <= 15: x_dot = 435
    elif len(full_name) <= 20: x_dot = 410
    elif len(full_name) <= 25: x_dot = 360
    elif len(full_name) <= 30: x_dot = 320
    elif len(full_name) <= 35: x_dot = 260
    else: x_dot = 185
    

    company = person.company

    if len(company) <= 10: x2_dot = 470
    elif len(company) <= 15: x2_dot = 425
    elif len(company) <= 20: x2_dot = 400
    elif len(company) <= 25: x2_dot = 350
    elif len(company) <= 30: x2_dot = 280
    elif len(company) <= 35: x2_dot = 250
    else: x2_dot = 185
    company = company.replace('”', '"')
    company = company.replace('“', '"')
    company = company.replace("’", "'")
    company = company.replace("‘", "'")
    district = person.region

    if district == None: district = ""
    else: district = district.title

    fa = FA.objects.get(code='FA')

    fa.count += 1
    fa.save()

    if len(str(fa.count)) == 1:
        cert = f"XT 0000{fa.count}"
    elif len(str(fa.count)) == 2:
        cert = f"XT 000{fa.count}"
    elif len(str(fa.count)) == 3:
        cert = f"XT 00{fa.count}"
    elif len(str(fa.count)) == 4:
        cert = f"XT 0{fa.count}"
    else:
        cert = f"{fa.count}"
    
    full_name = full_name.replace("’", "'")
    full_name = full_name.replace("‘", "'")
    full_name = full_name.replace('”', '"')
    full_name = full_name.replace('“', '"')

    cv2.putText(template, full_name, (x_dot, 415), cv2.FONT_HERSHEY_DUPLEX, 1.2, (150,10,10), 2, cv2.LINE_AA)
    cv2.putText(template, company, (x2_dot, 455), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(template, cert, (570, 365), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(template, district, (70, 730), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(template, str(person.date_certificate()), (145, 775), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

    qr_data = f"https://suvchimaktabi.uz/media/certificate/{person.certificate_id}.pdf"
    qr_code = generate_qr_code(qr_data)
    # Предположим, что мы хотим добавить QR-код в нижний правый угол
    qr_position = (template.shape[1] - qr_code.shape[1] - 50, template.shape[0] - qr_code.shape[0] - 50)
    add_qr_code_to_image(template, qr_code, qr_position)

    cv2.imwrite(str(BASE_DIR / f'media/certificate/{person.certificate_id}.jpg'), template)

    input_image_path = str(BASE_DIR / f'media/certificate/{person.certificate_id}.jpg')
    output_pdf_path = str(BASE_DIR / f'media/certificate/{person.certificate_id}.pdf')

    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    img_w, img_h = 297, 210
    pdf.image(input_image_path, x=0, y=0, w=img_w, h=img_h)
    pdf.output(output_pdf_path)
    
    file_to_delete = BASE_DIR / f'media/certificate/{person.certificate_id}.jpg'

    if file_to_delete.exists(): file_to_delete.unlink()

    person.pdf_created = True
    person.save()

    return True




@dramatiq.actor
def create_excel(excel_id, districts, date_filter_start, date_filter_end):

    excel = Excel.objects.get(id=excel_id)

    wb = Workbook()
    ws = wb.active

    headers = ['ФИО', 'Пол','Дата рождения','Организация','Номер телефона','ИНН','Сфера деятельности','Должность','Район','Регион','Платформа регистрации','Дата регистрации','Статус сертификата','Номер сертификата']
    ws.append(headers)

    students = Student.objects.filter(district_id__in=districts.split(':'), date_created__gte=date_filter_start, date_created__lte=date_filter_end)

    for s in students:
        ws.append([str(s.fio), str(s.gender), str(s.birthday), str(s.company), str(s.phone), str(s.inn), str(s.activity), str(s.job), str(s.region), str(s.district), str(s.platform), str(s.date_created_custom()), str(s.status), str(s.certificate_id)])


    random_name = ""
    for _ in range(10): random_name += random.choice('qwertyuiopasdfghjklzxcvbnm1234567890')
    excel.download = True
    excel.file = f"media/excel/{random_name}.xlsx"
    excel.save()
    wb.save(BASE_DIR / f"media/excel/{random_name}.xlsx")




# @dramatiq.actor
# def create_excel_umumiy():

#     wb = Workbook()
#     ws = wb.active

#     headers = ['ФИО','Пол','Дата рождения','Организация','Номер телефона','Сфера деятельности','Должность','Район','Регион','Платформа регистрации','Дата регистрации','Статус сертификата','Номер сертификата']
#     ws.append(headers)

#     students = Student.objects.all()

#     for s in students:
#         ws.append([str(s.fio), str(s.gender), str(s.birthday), str(s.company), str(s.phone), str(s.activity), str(s.job), str(s.region), str(s.district), str(s.platform), str(s.date_created_custom()), str(s.status), str(s.certificate_id)])

#     wb.save(BASE_DIR / "media/excel/umumiy.xlsx")
