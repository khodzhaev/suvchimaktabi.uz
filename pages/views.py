from django.shortcuts import render, get_object_or_404, redirect
from control.models import *
import json
from django.http import JsonResponse
import random
from control.tasks import generate_pdf
from django.conf import settings



# index html
def pages_index(request):
    office = Office.objects.last()
    news = News.objects.all()[:3]
    testimonials = Testimonial.objects.all()
    experts = Expert.objects.all()
    branchs = BranchForMap.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "news": news,
        "testimonials": testimonials,
        "captcha": captcha,
        "experts": experts,
        "branchs": branchs,
        "branchs_json": json.dumps(list(branchs.values("title", "address", "lat", "lon")))
    }

    return render(request, 'pages/index.html', context=data)


# about html
def pages_about(request):
    office = Office.objects.last()
    news = News.objects.all()[:3]
    staffs = Staff.objects.all()
    qas = QA.objects.all()
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "news": news,
        "staffs": staffs,
        "qas": qas,
        "experts": experts,
        "captcha": captcha
    }

    return render(request, 'pages/about.html', context=data)


# course
def pages_course(request):
    office = Office.objects.last()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()
    courses = Course.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "news": news,
        "experts": experts,
        "courses": courses,
        "captcha": captcha
    }

    return render(request, 'pages/course.html', context=data)



# course
def pages_course_fermer(request):
    office = Office.objects.last()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()
    courses = Course.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "news": news,
        "experts": experts,
        "courses": courses,
        "captcha": captcha
    }

    return render(request, 'pages/fermerlar.html', context=data)


def pages_course_loyihachi(request):
    office = Office.objects.last()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()
    courses = Course.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "news": news,
        "experts": experts,
        "courses": courses,
        "captcha": captcha
    }

    return render(request, 'pages/loyihachi.html', context=data)


# news html
def pages_news_all(request):
    office = Office.objects.last()
    news = News.objects.all()[:3]
    news_all = News.objects.all()
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "news": news,
        "news_all": news_all,
        "experts": experts,
        "captcha": captcha
    }

    return render(request, 'pages/news_all.html', context=data)


# news detail
def pages_news_detail(request, id):
    n = get_object_or_404(News, id=id)
    office = Office.objects.last()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "n": n,
        "office": office,
        "news": news,
        "experts": experts,
        "captcha": captcha
    }

    return render(request, 'pages/news_detail.html', context=data)


# gallery
def pages_gallery_all(request):
    office = Office.objects.last()
    galleries = Gallery.objects.all()
    emails = Email.objects.all()
    phones = Phone.objects.all()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "galleries": galleries,
        "office": office,
        'phones': phones,
        'emails': emails,
        'news': news,
        "experts": experts,
        "captcha": captcha
    }

    return render(request, 'pages/gallery_all.html', context=data)


def pages_gallery_detail(request, id):
    office = Office.objects.last()
    gallery = get_object_or_404(Gallery, id=id)
    emails = Email.objects.all()
    phones = Phone.objects.all()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "gallery": gallery,
        "office": office,
        'phones': phones,
        'emails': emails,
        'news': news,
        'cp': '/gallery/',
        "experts": experts,
        "captcha": captcha
    }

    return render(request, 'pages/gallery_detail.html', context=data)


# contact html
def pages_contact(request):
    office = Office.objects.last()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "news": news,
        "captcha": captcha,
        "experts": experts,
    }

    return render(request, 'pages/contact.html', context=data)


# book
def pages_books_category(request):
    office = Office.objects.last()
    categories = CategoryBook.objects.all()
    emails = Email.objects.all()
    phones = Phone.objects.all()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "categories": categories,
        "office": office,
        'phones': phones,
        'emails': emails,
        'news': news,
        "experts": experts,
        "captcha": captcha
    }

    return render(request, 'pages/books_category.html', context=data)


def pages_books(request, category_id):
    office = Office.objects.last()
    category = get_object_or_404(CategoryBook, id=category_id)
    books = Book.objects.filter(category=category)
    emails = Email.objects.all()
    phones = Phone.objects.all()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "books": books,
        "category": category,
        "office": office,
        'phones': phones,
        'emails': emails,
        'news': news,
        "experts": experts,
        "captcha": captcha
    }

    return render(request, 'pages/books.html', context=data)


# videos html
def pages_videos(request):
    office = Office.objects.last()
    videos = Video.objects.all()
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "videos": videos,
        "experts": experts,
        "captcha": captcha,
        "news": News.objects.all()[:3]
    }

    return render(request, 'pages/videos.html', context=data)



def pages_404(request, exception):
    office = Office.objects.last()
    news = News.objects.all()[:3]
    experts = Expert.objects.all()

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "news": news,
        "experts": experts,
        "captcha": captcha
    }

    return render(request, 'pages/404.html', context=data)


# contact feedback create
def pages_feedback_create(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try: captcha = Captcha.objects.all()[random.randint(1,100)]
        except: captcha = Captcha.objects.last()

        try:
            c = Captcha.objects.get(code=data['code'])

            if c.answer == data['answer']:
                FeedBack.objects.create(
                    fio = data["fio"],
                    phone = data["phone"],
                    email = data["email"],
                    message = data["message"]
                )

                return JsonResponse({"status": 200}, safe = False)
            else: return JsonResponse({"status": 404, 'code': captcha.code, 'answer': captcha.answer, 'image': captcha.image.url}, safe = False)
        except: return JsonResponse({"status": 404, 'code': captcha.code, 'answer': captcha.answer, 'image': captcha.image.url}, safe = False)
    else: return JsonResponse({"status": 404}, safe=False)


# qfe html
def pages_qfe(request):
    office = Office.objects.last()
    experts = Expert.objects.all()

    previous_experts = experts.filter(group='previous')
    current_experts = experts.filter(group='current')

    try: captcha = Captcha.objects.all()[random.randint(1,100)]
    except: captcha = Captcha.objects.last()

    data = {
        "office": office,
        "previous_experts": previous_experts,
        "current_experts": current_experts,
        "experts": experts,
        "captcha": captcha,
        "news": News.objects.all()[:3]
    }

    return render(request, 'pages/qfe.html', context=data)


# contact to expert create
def pages_qfe_create(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try: captcha = Captcha.objects.all()[random.randint(1,100)]
        except: captcha = Captcha.objects.last()

        try:
            c = Captcha.objects.get(code=data['code'])

            if c.answer == data['answer']:
                QFE.objects.create(
                    fio = data["fio"],
                    phone = data["phone"],
                    message = data["message"],
                    expert = get_object_or_404(Expert, id=data["s_id"])
                )

                return JsonResponse({"status": 200}, safe = False)
            else: return JsonResponse({"status": 404, 'code': captcha.code, 'answer': captcha.answer, 'image': captcha.image.url}, safe = False)
        except: return JsonResponse({"status": 404, 'code': captcha.code, 'answer': captcha.answer, 'image': captcha.image.url}, safe = False)
    else: return JsonResponse({"status": 404}, safe=False)


# refresh captcha
def pages_captcha_refresh(request):
    if request.method == 'POST':

        try: captcha = Captcha.objects.all()[random.randint(1,100)]
        except: captcha = Captcha.objects.last()

        return JsonResponse({"status": 200, 'code': captcha.code, 'answer': captcha.answer, 'image': captcha.image.url}, safe = False)
    return JsonResponse({"status": 404}, safe=False)

import base64
from django.core.files.base import ContentFile
# register
def pages_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # try: captcha = Captcha.objects.all()[random.randint(1,100)]
        # except: captcha = Captcha.objects.last()

        # try:
            # c = Captcha.objects.get(code=data['code'])

            # if c.answer == data['answer']:

        

        for i in Student.objects.all():
            if str(i.phone) == str(data["phone"]):
                return JsonResponse({"status": "exist"}, safe=False)

        s = Student.objects.create(
            fio = data["fio"],
            phone = data["phone"],
            region = get_object_or_404(Region, title = data["region"], available = True),
            district = get_object_or_404(District, title = data["district"], available = True),
            birthday = data["birthday"],
            gender = data["gender"],
            company = data["company"],
            activity = data["activity"],
            job = data["job"],
            inn = data['inn'],
            platform = "Web",
            status = "Сўровнома тўлдирилди",
            
        )

        try: 
            format, imgstr = data['file'].split(';base64,')
            ext = format.split('/')[-1]
            title = str(data["inn"])
            file = ContentFile(base64.b64decode(imgstr), name=f'{title}.' + ext)
            s.file=file
        except: pass
        s.certificate_id = s.id
        s.save()

        return JsonResponse({"status": 200, "id": s.id}, safe=False)
        #     else: return JsonResponse({"status": 404, 'code': captcha.code, 'answer': captcha.answer, 'image': captcha.image.url}, safe = False)
        # except: return JsonResponse({"status": 404, 'code': captcha.code, 'answer': captcha.answer, 'image': captcha.image.url}, safe = False)
    return JsonResponse({"status": 404}, safe=False)


def pages_phone_check(request):
    if request.method == "POST":
        data = json.loads(request.body)
        all_s_phones = list(map(lambda p: str(p.phone), Student.objects.all()))

        if data["phone"] in all_s_phones: return JsonResponse({"status": "used"}, safe=False)
        else: return JsonResponse({"status": "valid"}, safe=False)
    return JsonResponse({"status": 404}, safe=False)


def pages_inn_check(request):
    if request.method == "POST":
        data = json.loads(request.body)
        all_s_inns = list(map(lambda p: str(p.inn), Student.objects.all()))

        if data["inn"] in all_s_inns: return JsonResponse({"status": "used"}, safe=False)
        else: 
            company_name = ""
            with open(settings.BASE_DIR / 'companies.json', 'r', encoding='utf-8') as f:
                companies = json.load(f)

            for company in companies:
                if company["inn"] == data["inn"]:
                    company_name = company["name"]
                    break

            return JsonResponse({"status": "valid", "company_name": company_name}, safe=False)
    return JsonResponse({"status": 404}, safe=False)



# regions api
def pages_regions(request):
    regions = []

    for reg in Region.objects.filter(available=True):
        single_reg = {"title": reg.title, "districts": []}

        for dis in District.objects.filter(available=True, region=reg):
            single_reg["districts"].append({"title": dis.title})

        regions.append(single_reg)

    return JsonResponse({"regions": regions}, safe=False)


# certificate download
def pages_certificate_download(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            student = get_object_or_404(Student, certificate_id=data["c_id"])

            if student.completed or student.status == "Сертификат тайёр":
                if student.pdf_created:
                    return JsonResponse({"status": "redirected", "pdf_url": f"/media/certificate/{data['c_id']}.pdf"}, safe=False)
                else:
                    generate_pdf.send(data["c_id"])

                    student.pdf_created = True
                    student.save()

                    return JsonResponse({"status": "pdf_created"}, safe=False)
        except: return JsonResponse({"status": 404}, safe=False)
    return JsonResponse({"status": 404}, safe=False)


# program calendar ==============================

from datetime import date
import calendar

from django.utils.html import strip_tags


def programs_calendar(request):
    office = Office.objects.last()
    emails = Email.objects.all()
    phones = Phone.objects.all()
    news = News.objects.all()[:3]

    today = date.today()
    year = int(request.GET.get('year', today.year) or today.year)
    month = int(request.GET.get('month', today.month) or today.month)

    # Bound check
    if not (1 <= month <= 12):
        month = today.month

    years_qs = Program.objects.values_list('date', flat=True)
    years_set = sorted({d.year for d in years_qs if d}, reverse=True) or [today.year]
    if year not in years_set:
        years_set.insert(0, year)

    programs_month = Program.objects.filter(date__year=year, date__month=month).order_by('date')

    programs_by_day = {}
    programs_by_iso = {}
    for p in programs_month:
        day = p.date.day
        programs_by_day.setdefault(day, []).append(p)
        iso = p.date.isoformat()
        programs_by_iso.setdefault(iso, []).append({
            'id': p.id,
            'title_ru': p.title_ru or '',
            'title_uz': p.title_uz or '',
            'title_en': p.title_en or '',
            'snippet_ru': p.content_ru if p.content_ru else '',
            'snippet_uz': p.content_uz if p.content_uz else '',
            'snippet_en': p.content_en if p.content_en else '',
        })

    cal = calendar.Calendar(firstweekday=0)
    weeks = []
    for week in cal.monthdatescalendar(year, month):
        week_row = []
        for day_date in week:
            in_month = day_date.month == month
            week_row.append({
                'day': day_date.day,
                'in_month': in_month,
                'date': day_date,
                'iso': day_date.isoformat(),
                'is_today': day_date == today,
                'is_past': day_date < today,
                'programs': programs_by_day.get(day_date.day, []) if in_month else [],
            })
        weeks.append(week_row)

    context = {
        "office": office,
        "phones": phones,
        "emails": emails,
        "news": news,
        "year": year,
        "month": month,
        "years": years_set,
        "weeks": weeks,
        "today": today,
        "programs_json": json.dumps(programs_by_iso),
    }
    return render(request, "pages/calendar.html", context)