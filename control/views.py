from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import json
from django.http import JsonResponse, Http404
from django.core.paginator import InvalidPage, Paginator
from .tasks import generate_pdf, send_sms_notification, create_excel
from datetime import datetime, timedelta
from django.db.models import Q


###########################################################
# Base context
###########################################################
def base_context(request):
    try: code = request.build_absolute_uri().split('?')[1]
    except: code = None

    context = {"code": code}

    return context


###########################################################
# Account role check
###########################################################
def account_role_check(user):
    return True if user.account.districts == "0" else False


###########################################################
# Index
###########################################################

# index html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_index(request):
    phones = Phone.objects.all()
    emails = Email.objects.all()

    if Office.objects.last() is None:
        office = Office.objects.create()
    else:
        office = Office.objects.last()

    context = {
        "base": base_context(request),
        "office": office,
        "phones": phones,
        "emails": emails
    }

    return render(request, 'control/index.html', context)


# office edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_index_office_edit(request):
    if request.method == 'POST':
        office = Office.objects.last()

        office.address_ru = request.POST['address_ru']
        office.address_en = request.POST['address_en']
        office.address_uz = request.POST['address_uz']
        office.gmap = request.POST['gmap']
        office.email = request.POST['email']
        office.phone = request.POST['phone']
        office.youtube = request.POST['youtube']
        office.instagram = request.POST['instagram']
        office.facebook = request.POST['facebook']
        office.telegram = request.POST['telegram']
        office.telegram_bot = request.POST['telegram_bot']

        try:
            office.about_image = request.FILES['about_image']
        except: pass
        office.save()

        return redirect("/control/?success")
    return redirect("/control/?error")


# office phone create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_index_phone_create(request):
    if request.method == 'POST':

        Phone.objects.create(title=request.POST['phone'])

        return redirect("/control/?create")
    return redirect("/control/?error")


# office phone remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_index_phone_remove(request):
    if request.method == 'POST':

        Phone.objects.get(id=request.POST['id']).delete()

        return redirect("/control/?remove")
    return redirect("/control/?error")


# office email create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_index_email_create(request):
    if request.method == 'POST':

        Email.objects.create(title=request.POST['email'])

        return redirect("/control/?create")
    return redirect("/control/?error")


# office email remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_index_email_remove(request):
    if request.method == 'POST':

        Email.objects.get(id=request.POST['id']).delete()

        return redirect("/control/?remove")
    return redirect("/control/?error")


###########################################################
# Gallery folder
###########################################################

# gallery html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_gallery(request):
    folders = Gallery.objects.all()

    context = {
        "base": base_context(request),
        "folders": folders
    }

    return render(request, 'control/gallery/index.html', context)


# gallery folder add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_gallery_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/gallery/add.html', context)


# gallery detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_gallery_detail(request, id):
    folder = Gallery.objects.get(id=id)
    photos = GalleryPhoto.objects.filter(folder=folder)

    context = {
        "base": base_context(request),
        "folder": folder,
        "photos": photos,
    }

    return render(request, 'control/gallery/detail.html', context)


# gallery create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_gallery_create(request):
    if request.method == 'POST':

        Gallery.objects.create(
            priority = request.POST['priority'],
            title_ru = request.POST['title_ru'],
            title_en = request.POST['title_en'],
            title_uz = request.POST['title_uz']
        )

        return redirect("/control/gallery/?add")
    return redirect("/control/gallery/?error")


# gallery edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_gallery_edit(request):
    if request.method == 'POST':
        g = Gallery.objects.get(id=request.POST['id'])

        g.priority = request.POST['priority']
        g.title_ru = request.POST['title_ru']
        g.title_en = request.POST['title_en']
        g.title_uz = request.POST['title_uz']
        g.save()

        return redirect("/control/gallery/?success")
    return redirect("/control/gallery/?error")


# gallery remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_gallery_remove(request):
    if request.method == 'POST':

        Gallery.objects.get(id=request.POST['id']).delete()

        return redirect("/control/gallery/?remove")
    return redirect("/control/gallery/?error")


###########################################################
# Gallery photo
###########################################################

# photo create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_gallery_photo_create(request):
    if request.method == 'POST' and request.FILES["image"]:
        folder = Gallery.objects.get(id=request.POST['fid'])

        GalleryPhoto.objects.create(
            folder = folder,
            priority = request.POST['priority'],
            title_ru = request.POST['title_ru'],
            title_en = request.POST['title_en'],
            title_uz = request.POST['title_uz'],
            image = request.FILES['image']
        )

        return redirect(f"/control/gallery/{folder.id}/?p_create")
    return redirect(f"/control/gallery/{folder.id}/?error")


# photo edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_gallery_photo_edit(request):
    if request.method == 'POST':
        p = GalleryPhoto.objects.get(id=request.POST['id'])

        p.priority = request.POST['priority']
        p.title_ru = request.POST['title_ru']
        p.title_en = request.POST['title_en']
        p.title_uz = request.POST['title_uz']

        try: p.image = request.FILES['image']
        except: pass

        p.save()

        return redirect(f"/control/gallery/{request.POST['fid']}/?p_edit")
    return redirect(f"/control/gallery/{request.POST['fid']}/?error")


# photo remove 
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_gallery_photo_remove(request):
    if request.method == 'POST':

        GalleryPhoto.objects.get(id=request.POST['id']).delete()

        return redirect(f"/control/gallery/{request.POST['fid']}/?p_remove")
    return redirect(f"/control/gallery/{request.POST['fid']}/?error")


###########################################################
# News
###########################################################

# news html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_news(request):
    news = News.objects.all()

    context = {
        "base": base_context(request),
        "news": news,
    }

    return render(request, 'control/news/index.html', context)


# news add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_news_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/news/add.html', context)


# news detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_news_detail(request, id):
    news = News.objects.get(id=id)

    context = {
        "base": base_context(request),
        "news": news
    }

    return render(request, 'control/news/detail.html', context)


# news create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_news_create(request):
    if request.method == 'POST' and request.FILES['image']:

        News.objects.create(
            date_created = request.POST['date'],
            title_ru = request.POST['title_ru'],
            title_en = request.POST['title_en'],
            title_uz = request.POST['title_uz'],
            content_en = request.POST['content_en'],
            content_ru = request.POST['content_ru'],
            content_uz = request.POST['content_uz'],
            image = request.FILES['image']
        )

        return redirect("/control/news/?add")
    return redirect("/control/news/?error")


# news edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_news_edit(request):
    if request.method == 'POST':
        n = News.objects.get(id=request.POST['id'])

        n.date_created = request.POST['date']
        n.title_ru = request.POST['title_ru']
        n.title_en = request.POST['title_en']
        n.title_uz = request.POST['title_uz']
        n.content_en = request.POST['content_en']
        n.content_ru = request.POST['content_ru']
        n.content_uz = request.POST['content_uz']

        try: n.image = request.FILES['image']
        except: pass

        n.save()

        return redirect("/control/news/?success")
    return redirect("/control/news/?error")


# news remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_news_remove(request):
    if request.method == 'POST':

        News.objects.get(id=request.POST['id']).delete()

        return redirect("/control/news/?remove")
    return redirect("/control/news/?error")


###########################################################
# Staff
###########################################################

# staff html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_staff(request):
    staffs = Staff.objects.all()

    context = {
        "base": base_context(request),
        "staffs": staffs,
    }

    return render(request, 'control/staff/index.html', context)


# staff add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_staff_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/staff/add.html', context)


# staff detail 
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_staff_detail(request, id):
    staff = Staff.objects.get(id=id)

    context = {
        "base": base_context(request),
        "staff": staff
    }

    return render(request, 'control/staff/detail.html', context)


# staff create 
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_staff_create(request):
    if request.method == 'POST' and request.FILES["image"]:

        Staff.objects.create(
            priority = request.POST['priority'],
            fio_ru = request.POST['title_ru'],
            fio_en = request.POST['title_en'],
            fio_uz = request.POST['title_uz'],
            profession_en = request.POST['profession_en'],
            profession_ru = request.POST['profession_ru'],
            profession_uz = request.POST['profession_uz'],
            image = request.FILES['image'],
        )

        return redirect("/control/staff/?add")
    return redirect("/control/staff/?error")


# staff edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_staff_edit(request):
    if request.method == 'POST':
        s = Staff.objects.get(id=request.POST['id'])

        s.priority = request.POST['priority']
        s.fio_ru = request.POST['title_ru']
        s.fio_en = request.POST['title_en']
        s.fio_uz = request.POST['title_uz']
        s.profession_en = request.POST['profession_en']
        s.profession_ru = request.POST['profession_ru']
        s.profession_uz = request.POST['profession_uz']

        try: s.image = request.FILES['image']
        except: pass

        s.save()

        return redirect("/control/staff/?success")
    return redirect("/control/staff/?error")


# staff remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_staff_remove(request):
    if request.method == 'POST':

        Staff.objects.get(id=request.POST['id']).delete()

        return redirect("/control/staff/?remove")
    return redirect("/control/staff/?error")


###########################################################
# Expert
###########################################################

# expert html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_expert(request):
    experts = Expert.objects.all()

    context = {
        "base": base_context(request),
        "experts": experts,
    }

    return render(request, 'control/expert/index.html', context)


# expert add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_expert_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/expert/add.html', context)


# expert detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_expert_detail(request, id):
    expert = Expert.objects.get(id=id)

    context = {
        "base": base_context(request),
        "expert": expert
    }

    return render(request, 'control/expert/detail.html', context)


# expert create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_expert_create(request):
    if request.method == 'POST' and request.FILES["image"]:

        Expert.objects.create(
            group = request.POST['group'],
            priority = request.POST['priority'],
            fio_ru = request.POST['title_ru'],
            fio_en = request.POST['title_en'],
            fio_uz = request.POST['title_uz'],
            profession_en = request.POST['profession_en'],
            profession_ru = request.POST['profession_ru'],
            profession_uz = request.POST['profession_uz'],
            direction_en = request.POST['direction_en'],
            direction_ru = request.POST['direction_ru'],
            direction_uz = request.POST['direction_uz'],
            image = request.FILES['image'],
        )

        return redirect("/control/expert/?add")
    return redirect("/control/expert/?error")


# expert edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_expert_edit(request):
    if request.method == 'POST':
        s = Expert.objects.get(id=request.POST['id'])

        s.group = request.POST['group']
        s.priority = request.POST['priority']
        s.fio_ru = request.POST['title_ru']
        s.fio_en = request.POST['title_en']
        s.fio_uz = request.POST['title_uz']
        s.profession_en = request.POST['profession_en']
        s.profession_ru = request.POST['profession_ru']
        s.profession_uz = request.POST['profession_uz']
        s.direction_en = request.POST['direction_en']
        s.direction_ru = request.POST['direction_ru']
        s.direction_uz = request.POST['direction_uz']

        try: s.image = request.FILES['image']
        except: pass

        s.save()

        return redirect("/control/expert/?success")
    return redirect("/control/expert/?error")


# expert remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_expert_remove(request):
    if request.method == 'POST':

        Expert.objects.get(id=request.POST['id']).delete()

        return redirect("/control/expert/?remove")
    return redirect("/control/expert/?error")


###########################################################
# Testimonials
###########################################################

# testimonial html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_testi(request):
    testi = Testimonial.objects.all()

    context = {
        "base": base_context(request),
        "testi": testi
    }

    return render(request, 'control/testi/index.html', context)


# testimonial add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_testi_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/testi/add.html', context)


# testimonial detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_testi_detail(request, id):
    testi = Testimonial.objects.get(id=id)

    context = {
        "base": base_context(request),
        "testi": testi
    }

    return render(request, 'control/testi/detail.html', context)


# testimonial create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_testi_create(request):
    if request.method == 'POST' and request.FILES["image"]:

        Testimonial.objects.create(
            content = request.POST['content'],
            fio_ru = request.POST['fio'],
            fio_uz = request.POST['fio_uz'],
            fio_en = request.POST['fio_en'],
            profession_ru = request.POST['proffesion'],
            profession_en = request.POST['proffesion_en'],
            profession_uz = request.POST['proffesion_uz'],
            priority = request.POST['priority'],
            image = request.FILES['image']
        )

        return redirect("/control/testi/?add")
    return redirect("/control/testi/?error")


# testimonial edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_testi_edit(request):
    if request.method == 'POST':
        t = Testimonial.objects.get(id=request.POST['id'])

        t.content = request.POST['content']
        t.fio_ru = request.POST['fio']
        t.fio_uz = request.POST['fio_uz']
        t.fio_en = request.POST['fio_en']
        t.profession_ru = request.POST['proffesion']
        t.profession_uz = request.POST['proffesion_uz']
        t.profession_en = request.POST['proffesion_en']
        t.priority = request.POST['priority']

        try: t.image = request.FILES['image']
        except: pass

        t.save()

        return redirect("/control/testi/?success")
    return redirect("/control/testi/?error")


# testimonial remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_testi_remove(request):
    if request.method == 'POST':

        Testimonial.objects.get(id=request.POST['id']).delete()

        return redirect("/control/testi/?remove")
    return redirect("/control/testi/?error")


###########################################################
# QA
###########################################################

# qa html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_qa(request):
    qas = QA.objects.all()

    context = {
        "base": base_context(request),
        "qas": qas,
    }

    return render(request, 'control/qa/index.html', context)


# qa add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_qa_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/qa/add.html', context)


# qa detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_qa_detail(request, id):
    qa = QA.objects.get(id=id)

    context = {
        "base": base_context(request),
        "qa": qa
    }

    return render(request, 'control/qa/detail.html', context)


# qa create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_qa_create(request):
    if request.method == 'POST':

        QA.objects.create(
            priority = request.POST['priority'],
            title_ru = request.POST['title_ru'],
            title_en = request.POST['title_en'],
            title_uz = request.POST['title_uz'],
            content_en = request.POST['content_en'],
            content_ru = request.POST['content_ru'],
            content_uz = request.POST['content_uz'],
        )

        return redirect("/control/qa/?add")
    return redirect("/control/qa/?error")


# qa edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_qa_edit(request):
    if request.method == 'POST':
        n = QA.objects.get(id=request.POST['id'])

        n.priority = request.POST['priority']
        n.title_ru = request.POST['title_ru']
        n.title_en = request.POST['title_en']
        n.title_uz = request.POST['title_uz']
        n.content_en = request.POST['content_en']
        n.content_ru = request.POST['content_ru']
        n.content_uz = request.POST['content_uz']

        n.save()

        return redirect("/control/qa/?success")
    return redirect("/control/qa/?error")


# qa remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_qa_remove(request):
    if request.method == 'POST':

        QA.objects.get(id=request.POST['id']).delete()

        return redirect("/control/qa/?remove")
    return redirect("/control/qa/?error")


###########################################################
# Course
###########################################################

# course html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_course(request):
    courses = Course.objects.all()

    context = {
        "base": base_context(request),
        "courses": courses,
    }

    return render(request, 'control/course/index.html', context)


# course add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_course_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/course/add.html', context)


# course detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    context = {
        "base": base_context(request),
        "course": course
    }

    return render(request, 'control/course/detail.html', context)


# course create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_course_create(request):
    if request.method == 'POST' and request.FILES['image']:

        Course.objects.create(
            title_ru = request.POST['title_ru'],
            title_en = request.POST['title_en'],
            title_uz = request.POST['title_uz'],
            content_en = request.POST['content_en'],
            content_ru = request.POST['content_ru'],
            content_uz = request.POST['content_uz'],
            priority = request.POST['priority'],
            time_interval = request.POST['time_interval'],
            image = request.FILES['image']
        )

        return redirect("/control/course/?add")
    return redirect("/control/course/?error")


# course edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_course_edit(request):
    if request.method == 'POST':
        n = get_object_or_404(Course, id=request.POST['id'])

        n.priority = request.POST['priority']
        n.title_ru = request.POST['title_ru']
        n.title_en = request.POST['title_en']
        n.title_uz = request.POST['title_uz']
        n.content_en = request.POST['content_en']
        n.content_ru = request.POST['content_ru']
        n.content_uz = request.POST['content_uz']
        n.time_interval = request.POST['time_interval']

        try: n.image = request.FILES['image']
        except: pass

        n.save()

        return redirect("/control/course/?success")
    return redirect("/control/course/?error")


# course remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_course_remove(request):
    if request.method == 'POST':

        Course.objects.get(id=request.POST['id']).delete()

        return redirect("/control/course/?remove")
    return redirect("/control/course/?error")


###########################################################
# Feedback
###########################################################

# feedback html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_feedback(request):
    feedbacks = FeedBack.objects.all()

    context = {
        "base": base_context(request),
        "feedbacks": feedbacks
    }

    return render(request, 'control/feedback.html', context)


# feedback remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_feedback_remove(request):
    if request.method == 'POST':

        FeedBack.objects.get(id=request.POST['id']).delete()

        return redirect("/control/feedback/?remove")
    return redirect("/control/feedback/?error")


###########################################################
# Users
###########################################################

# users html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_users(request):
    users = User.objects.all()

    context = {
        "base": base_context(request),
        "users": users,
    }

    return render(request, 'control/users/index.html', context)


# user add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_users_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/users/add.html', context)


# user detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_users_detail(request):
    context = {"base": base_context(request)}

    return render(request, 'control/users/detail.html', context)


# user create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_users_create(request):
    if request.method == 'POST':
        users = User.objects.all()

        for i in users:
            if str(i.username) == str(request.POST['phone']):
                return redirect("/control/users/add/?exist")

        u = User.objects.create_user(
            username = request.POST['phone'],
            first_name = request.POST['fio'],
            password = request.POST['password'],
        )

        a = Account.objects.get(user=u)
        a.districts = request.POST["selected_districts"]
        a.save()

        return redirect("/control/users/?add")
    return redirect("/control/users/add/?error")


# user edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_users_edit(request):
    if request.method == 'POST':
        u = User.objects.get(id=request.POST['id'])

        u.set_password(request.POST['password'])
        u.save()

        return redirect("/control/users/?success")
    return redirect("/control/users/?error")


# user remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_users_remove(request):
    if request.method == 'POST':

        User.objects.get(id=request.POST['id']).delete()

        return redirect("/control/users/?remove")
    return redirect("/control/users/?error")


# user districts api
@login_required(login_url="login_index")
def control_user_districts_api(request):
    if request.method == "POST":
        answer = {"status": 200, "all_reg": []}

        for r in Region.objects.filter(available=True):
            s_r = {"title": r.title, "id": r.id, "districts": [], "all_selected": False}

            for d in District.objects.filter(region=r, available=True):
                s_r["districts"].append({"id": d.id, "title": d.title, "r_id": r.id, "selected": False})

            answer["all_reg"].append(s_r)

        return JsonResponse(answer, safe=False)
    else: return JsonResponse({"status": 404}, safe=False)


###########################################################
# Region
###########################################################

# regions html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_region(request):
    regions = Region.objects.filter(available=True)

    context = {
        "base": base_context(request),
        "regions": regions
    }

    return render(request, 'control/region/index.html', context)


# regions add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_region_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/region/add.html', context)


# regions detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_region_detail(request, id):
    region = Region.objects.get(id=id, available=True)

    context = {
        "base": base_context(request),
        "region": region,
    }

    return render(request, 'control/region/detail.html', context)


# regions create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_region_create(request):
    if request.method == 'POST':

        for i in Region.objects.filter(available=True):
            if i.title.lower() == request.POST["title"].lower():
                return redirect("/control/region/add/?exist")

        Region.objects.create(title = request.POST['title'])

        return redirect("/control/region/?add")
    return redirect("/control/region/?error")


# regions edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_region_edit(request):
    if request.method == 'POST':
        g = Region.objects.get(id=request.POST['id'], available=True)

        for i in Region.objects.filter(available=True):
            if i.title.lower() == request.POST["title"].lower() and i.id != g.id:
                return redirect(f"/control/region/{g.id}/?exist")

        g.title = request.POST['title']
        g.save()

        return redirect("/control/region/?success")
    return redirect("/control/region/?error")


# regions remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_region_remove(request):
    if request.method == 'POST':
        r = Region.objects.get(id=request.POST['id'])

        r.available = False
        r.save()

        return redirect("/control/region/?remove")
    return redirect("/control/region/?error")


###########################################################
# District
###########################################################

# district html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_district(request):
    districts = District.objects.filter(available=True)

    context = {
        "base": base_context(request),
        "districts": districts
    }

    return render(request, 'control/district/index.html', context)


# district add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_district_add(request):
    regions = Region.objects.filter(available=True)

    context = {
        "base": base_context(request),
        "regions": regions
    }

    return render(request, 'control/district/add.html', context)


# district detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_district_detail(request, id):
    regions = Region.objects.filter(available=True)
    district = District.objects.get(id=id, available=True)

    context = {
        "base": base_context(request),
        "regions": regions,
        "district": district
    }

    return render(request, 'control/district/detail.html', context)


# district create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_district_create(request):
    if request.method == 'POST':

        try: region = Region.objects.get(id=request.POST["region_id"], available=True)
        except: return redirect("/control/district/add/?error")

        for i in District.objects.filter(available=True):
            if i.title.lower() == request.POST["title"].lower():
                return redirect("/control/district/add/?exist")

        District.objects.create(
            title = request.POST['title'],
            region = region
        )

        return redirect("/control/district/?add")
    return redirect("/control/district/?error")


# district edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_district_edit(request):
    if request.method == 'POST':
        g = District.objects.get(id=request.POST["id"], available=True)

        try: region = Region.objects.get(id=request.POST["region_id"], available=True)
        except: return redirect(f"/control/district/{g.id}/?error")

        for i in District.objects.filter(available=True):
            if i.title.lower() == request.POST["title"].lower() and i.id != g.id:
                return redirect(f"/control/district/{g.id}/?exist")

        g.region = region
        g.title = request.POST['title']
        g.save()

        return redirect("/control/district/?success")
    return redirect("/control/district/?error")


# district remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_district_remove(request):
    if request.method == 'POST':
        r = District.objects.get(id=request.POST['id'])

        r.available = False
        r.save()

        return redirect("/control/district/?remove")
    return redirect("/control/district/?error")


###########################################################
# Students
###########################################################

# students html
@login_required(login_url="login_index")
def control_students(request):
    districts = request.user.account.districts
    office = Office.objects.last()

    try: search = request.GET.get("search").lower().strip()
    except: search = False

    try: status = request.GET.get("status")
    except: status = False

    if len(districts):
        if districts == "0":
            students = Student.objects.all()

            all_s = office.get_students_count()
            completed_s = office.get_completed_students_count()
            registered_s = office.get_registered_students_count()
            registering_s = office.get_registering_students_count()
        else:
            allowed_ids = []

            for i in districts.split(":"): allowed_ids.append(int(i))

            students = Student.objects.filter(district_id__in=allowed_ids)

            all_s = students.count()
            completed_s = 0

            for i in students:
                if i.status == "Сертификат тайёр" or i.completed: completed_s+=1

            registered_s = Student.objects.filter(
                district_id__in=allowed_ids, status="Сўровнома тўлдирилди"
            ).count()

            registering_s = Student.objects.filter(
                district_id__in=allowed_ids, status="Рўйхатдан ўтмоқда"
            ).count()
    else: return render(request, "control/students.html", {"status": "not_allowed"})

    if search:
        students = students.filter(Q(fio__icontains=search) | Q(phone__icontains=search))

    if status and status != "all":

        if status == "completed": t_status = "Сертификат тайёр"
        elif status == "registered": t_status = "Сўровнома тўлдирилди"
        elif status == "registering": t_status = "Рўйхатдан ўтмоқда"

        students = students.filter(status=t_status)

    paginator = Paginator(students, 200, orphans=5)
    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get("page") or 1

    try: current_page = paginator.page(page)
    except InvalidPage as e: raise Http404(str(e))

    context = {
        "current_page": current_page,
        "is_paginated": is_paginated,
        "paginator": paginator,
        "search": search,
        "status": status,
        "all_s": all_s,
        "completed_s": completed_s,
        "registered_s": registered_s,
        "registering_s": registering_s,
    }

    return render(request, "control/students.html", context)


# student status change
@login_required(login_url="login_index")
def control_students_status_change(request):
    if request.method == "POST":
        data = json.loads(request.body)
        s = Student.objects.get(id = data["id"])

        s.status = data["status"]
        s.completed = True
        s.date_confirmed = datetime.now()
        s.save()

        generate_pdf.send(s.certificate_id)
        send_sms_notification.send(s.phone, s.certificate_id)

        return JsonResponse({"status": 200}, safe=False)
    else: return JsonResponse({"status": 404}, safe=False)


# student delete
@login_required(login_url="login_index")
def control_students_delete(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Student.objects.get(id = data["id"]).delete()

        return JsonResponse({"status": 200}, safe=False)
    else: return JsonResponse({"status": 404}, safe=False)

import base64
from django.core.files.base import ContentFile
# student edit
@login_required(login_url="login_index")
def control_students_edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        s = Student.objects.get(id = data["id"])

        if s.fio != data['fio']:
            s.pdf_created = False

        s.phone = data["phone"]
        s.fio = data["fio"]
        s.company = data["company"]
        s.activity = data["activity"]
        s.birthday = data["birthday"]
        s.gender = data["gender"]
        s.job = data["job"]
        s.inn = data['inn']
        s.region = get_object_or_404(Region, id=data["region_id"])
        s.district = get_object_or_404(District, id=data["district_id"])

        if data['filez']:
            format, imgstr = data['filez'].split(';base64,')
            ext = format.split('/')[-1]
            title = str(data["inn"])
            file = ContentFile(base64.b64decode(imgstr), name=f'{title}.' + ext)
        
            s.file = file
        s.save()

        return JsonResponse({"status": 'ok'}, safe=False)
    else: return JsonResponse({"status": 404}, safe=False)


# student certificate download
@login_required(login_url="login_index")
def control_students_certificate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student = get_object_or_404(Student, id=data["id"])
        c_id = str(student.certificate_id)

        if student.completed or student.status == "Сертификат тайёр":
            if student.pdf_created:
                return JsonResponse({"status": "redirected", "pdf_url": f"/media/certificate/{c_id}.pdf"}, safe=False)
            else:
                generate_pdf.send(c_id)

                return JsonResponse({"status": "pdf_created"}, safe=False)
    return JsonResponse({"status": 404}, safe=False)


# student send sms
@login_required(login_url="login_index")
def control_students_sms_send(request):
    if request.method == "POST":
        data = json.loads(request.body)
        s = Student.objects.get(id=data['id'])

        if s.pdf_created == False: generate_pdf.send(s.certificate_id)

        send_sms_notification.send(s.phone, s.certificate_id)

        return JsonResponse({"status": 200}, safe=False)
    else: return JsonResponse({"status": 404}, safe=False)


# student excel
@login_required(login_url="login_index")
def control_students_excel(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # if request.user.last_name == '0':
        #     students = Student.objects.filter(date_created__gte=data['from'], date_created__lte=data['to'])
        # else:
        #     students = Student.objects.filter(district_id__in=request.user.last_name.split(':'), date_created__gte=data['from'], date_created__lte=data['to'])

        date_filter_start = datetime.strptime(data['from'], "%Y-%m-%d")
        date_filter_end = date_filter_start + timedelta(days=1)

        if request.user.account.districts == '0':
            students = Student.objects.filter(date_created__gte=date_filter_start, date_created__lt=date_filter_end)
        else:
            students = Student.objects.filter(district_id__in=request.user.account.districts.split(':'), date_created__gte=date_filter_start, date_created__lt=date_filter_end)

        data = [["ФИО", "Пол", "Дата рождения", "Организация", "Номер телефона", "ИНН", "Сфера деятельности", "Должность", "Район", "Регион", "Платформа", "Дата регистрации", "Статус сертификата","Номер сертификата"]]

        for s in students:
            data.append([str(s.fio), str(s.gender), str(s.birthday), str(s.company), str(s.phone), str(s.inn), str(s.activity), str(s.job), str(s.region), str(s.district), str(s.platform), str(s.date_created_custom()), str(s.status), str(s.certificate_id)])

        return JsonResponse({"status": 200, 'data': data}, safe=False)
    else: return JsonResponse({"status": 404}, safe=False)


###########################################################
# Question for expert
###########################################################

# qfe html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_qfe(request):
    qfes = QFE.objects.all()

    context = {
        "base": base_context(request),
        "qfes": qfes,
    }

    return render(request, 'control/qfe.html', context)


# qfe remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_qfe_remove(request):
    if request.method == 'POST':

        QFE.objects.get(id=request.POST['id']).delete()

        return redirect("/control/qfe/?remove")
    return redirect("/control/qfe/?error")


###########################################################
# Excel
###########################################################

# excel html
@login_required(login_url="login_index")
def control_excel(request):
    excels = Excel.objects.filter(user=request.user)

    if excels.first(): waiting = False if excels.first().download else True
    else: waiting = False

    context = {
        "base": base_context(request),
        "excels": excels,
        "waiting": waiting
    }

    return render(request, 'control/excel.html', context)


# excel remove
@login_required(login_url="login_index")
def control_excel_remove(request):
    if request.method == 'POST':

        Excel.objects.get(id=request.POST['id'], user=request.user).delete()

        return redirect("/control/excel/?remove")
    return redirect("/control/excel/?error")


# excel create
@login_required(login_url="login_index")
def control_excel_create(request):
    if request.method == 'POST':
        d_from = request.POST["from"]
        d_until = request.POST["until"]
        districts = request.POST["selected_districts"]

        # print(d_from)
        # print(d_until)
        # print(districts) # .split(":")

        e = Excel.objects.create(
            user=request.user,
            title=f"{d_from} => {d_until}",
        )

        create_excel.send(excel_id=e.id, districts=districts, date_filter_start=d_from, date_filter_end=d_until)

        return redirect("/control/excel/?created")
    return redirect("/control/excel/?error")


# download all data
# @login_required(login_url="login_index")
# def control_excel_umumiy(request):
#     create_excel_umumiy.send()
#     return redirect("/control/excel/?created")


###########################################################
# Book
###########################################################

# book html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_book(request):
    books = Book.objects.all()

    context = {
        "base": base_context(request),
        "books": books
    }

    return render(request, 'control/book/index.html', context)


# book add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_book_add(request):
    categories = CategoryBook.objects.all()

    context = {
        "base": base_context(request),
        'categories': categories}

    return render(request, 'control/book/add.html', context)


# book detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_book_detail(request, id):
    book = Book.objects.get(id=id)
    categories = CategoryBook.objects.all()

    context = {
        "base": base_context(request),
        "book": book,
        'categories': categories
    }

    return render(request, 'control/book/detail.html', context)


# book create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_book_create(request):
    if request.method == 'POST' and request.FILES["file"]:

        Book.objects.create(
            priority = request.POST['priority'],
            category = CategoryBook.objects.get(id=request.POST['category_id']),
            title_ru = request.POST['title_ru'],
            title_uz = request.POST['title_uz'],
            title_en = request.POST['title_en'],
            pdf = request.FILES['file']
        )

        return redirect(f"/control/book/?add")
    return redirect(f"/control/book/?error")


# book edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_book_edit(request):
    if request.method == 'POST':
        p = Book.objects.get(id=request.POST['id'])

        p.priority = request.POST['priority']
        p.category = CategoryBook.objects.get(id=request.POST['category_id'])

        p.title_ru = request.POST['title_ru']
        p.title_uz = request.POST['title_uz']
        p.title_en = request.POST['title_en']

        try: p.pdf = request.FILES['file']
        except: pass

        p.save()

        return redirect(f"/control/book/?edit")
    return redirect(f"/control/book/?error")


# book remove 
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_book_remove(request):
    if request.method == 'POST':

        Book.objects.get(id=request.POST['id']).delete()

        return redirect(f"/control/book/?remove")
    return redirect(f"/control/book/?error")



###########################################################
# Video
###########################################################

# video html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_video(request):
    videos = Video.objects.all()

    context = {
        "base": base_context(request),
        "videos": videos,
    }

    return render(request, 'control/video/index.html', context)


# video add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_video_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/video/add.html', context)


# video detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_video_detail(request, id):
    video = get_object_or_404(Video, id=id)

    context = {
        "base": base_context(request),
        "video": video
    }

    return render(request, 'control/video/detail.html', context)


# video create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_video_create(request):
    if request.method == 'POST' and request.FILES['image']:

        Video.objects.create(
            title_ru = request.POST['title_ru'],
            title_en = request.POST['title_en'],
            title_uz = request.POST['title_uz'],
            priority = request.POST['priority'],
            url = request.POST['url'],
            image = request.FILES['image']
        )

        return redirect("/control/video/?add")
    return redirect("/control/video/?error")


# video edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_video_edit(request):
    if request.method == 'POST':
        n = get_object_or_404(Video, id=request.POST['id'])

        n.priority = request.POST['priority']
        n.title_ru = request.POST['title_ru']
        n.title_en = request.POST['title_en']
        n.title_uz = request.POST['title_uz']
        n.url = request.POST['url']

        try: n.image = request.FILES['image']
        except: pass

        n.save()

        return redirect("/control/video/?success")
    return redirect("/control/video/?error")


# video remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_video_remove(request):
    if request.method == 'POST':

        Video.objects.get(id=request.POST['id']).delete()

        return redirect("/control/video/?remove")
    return redirect("/control/video/?error")



###########################################################
# Program
###########################################################

# program html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_program(request):
    programs = Program.objects.all()

    context = {
        "base": base_context(request),
        "programs": programs,
    }

    return render(request, 'control/program/index.html', context)


# program add html
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_program_add(request):
    context = {"base": base_context(request)}

    return render(request, 'control/program/add.html', context)


# program detail
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_program_detail(request, id):
    program = get_object_or_404(Program, id=id)

    context = {
        "base": base_context(request),
        "program": program
    }

    return render(request, 'control/program/detail.html', context)


# program create
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_program_create(request):
    if request.method == 'POST':

        Program.objects.create(
            title_ru = request.POST['title_ru'],
            title_en = request.POST['title_en'],
            title_uz = request.POST['title_uz'],
            content_en = request.POST['content_en'],
            content_ru = request.POST['content_ru'],
            content_uz = request.POST['content_uz'],
            date = request.POST['date'],
        )

        return redirect("/control/program/?add")
    return redirect("/control/program/?error")


# program edit
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_program_edit(request):
    if request.method == 'POST':
        n = get_object_or_404(Program, id=request.POST['id'])

        n.title_ru = request.POST['title_ru']
        n.title_en = request.POST['title_en']
        n.title_uz = request.POST['title_uz']
        n.content_en = request.POST['content_en']
        n.content_ru = request.POST['content_ru']
        n.content_uz = request.POST['content_uz']
        n.date = request.POST['date']

        n.save()

        return redirect("/control/program/?success")
    return redirect("/control/program/?error")


# program remove
@login_required(login_url="login_index")
@user_passes_test(account_role_check, login_url='login_index')
def control_program_remove(request):
    if request.method == 'POST':

        Program.objects.get(id=request.POST['id']).delete()

        return redirect("/control/program/?remove")
    return redirect("/control/program/?error")




############################
from django.http import HttpResponse, Http404
from django.conf import settings
import os

def certificate_view(request, certificate_code):
    # Путь к папке media
    media_root = settings.MEDIA_ROOT
    fff = certificate_code.split('-')[1]
    # Строим путь к файлу внутри media
    file_path = os.path.join(media_root, f"L/{fff}.pdf")  # предположим, что это PDF файл

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{fff}.pdf"'
            return response
    else:
        raise Http404("Файл не найден")






def certificate_view_a(request, certificate_code):
    # Путь к папке media
    fff = certificate_code.split('-')[1]
    return redirect(f'/media/A/{fff}.jpg')
