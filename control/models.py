from django.db import models
from django_resized import ResizedImageField
from dateutil import tz, parser
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User


###########################################################
# News
###########################################################
class News(models.Model):
    title_ru = models.CharField(max_length=255)
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    content_ru = models.TextField()
    content_uz = models.TextField()
    content_en = models.TextField()
    image = ResizedImageField(size=[740, 460], upload_to='news/', null=True, blank=True)
    watch_count = models.BigIntegerField(default=0)
    date_created = models.DateField()

    def html_date(self):
        return self.date_created.strftime('%Y-%m-%d')

    class Meta:
        ordering = ('-date_created',)


###########################################################
# QA
###########################################################
class QA(models.Model):
    title_ru = models.CharField(max_length=500, null=True, blank=True)
    title_uz = models.CharField(max_length=500, null=True, blank=True)
    title_en = models.CharField(max_length=500, null=True, blank=True)
    content_ru = models.TextField()
    content_uz = models.TextField()
    content_en = models.TextField()
    priority = models.IntegerField(default=1)

    class Meta:
        ordering = ('priority',)


###########################################################
# Testimonial
###########################################################
class Testimonial(models.Model):
    fio_ru = models.CharField(max_length=255, null=True, blank=True)
    fio_uz = models.CharField(max_length=255, null=True, blank=True)
    fio_en = models.CharField(max_length=255, null=True, blank=True)
    profession_ru = models.CharField(max_length=255, null=True, blank=True)
    profession_uz = models.CharField(max_length=255, null=True, blank=True)
    profession_en = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    image = ResizedImageField(size=[340, 400], upload_to='testimonial/', null=True, blank=True)
    priority = models.IntegerField(default=1)

    class Meta:
        ordering = ('priority',)


###########################################################
# Staff
###########################################################
class Staff(models.Model):
    fio_ru = models.CharField(max_length=255, null=True, blank=True)
    fio_uz = models.CharField(max_length=255, null=True, blank=True)
    fio_en = models.CharField(max_length=255, null=True, blank=True)
    profession_ru = models.CharField(max_length=255, null=True, blank=True)
    profession_uz = models.CharField(max_length=255, null=True, blank=True)
    profession_en = models.CharField(max_length=255, null=True, blank=True)
    image = ResizedImageField(size=[600, 600], upload_to='staff/', null=True, blank=True)
    priority = models.IntegerField(default=1)

    class Meta:
        ordering = ('priority',)


###########################################################
# Expert
###########################################################
class Expert(models.Model):
    GROUP_CHOICES = [
        ('previous', 'Бывший коллега'),
        ('current', 'Текущий коллега'),
    ]
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='current')
    fio_ru = models.CharField(max_length=255, null=True, blank=True)
    fio_uz = models.CharField(max_length=255, null=True, blank=True)
    fio_en = models.CharField(max_length=255, null=True, blank=True)
    profession_ru = models.CharField(max_length=255, null=True, blank=True)
    profession_uz = models.CharField(max_length=255, null=True, blank=True)
    profession_en = models.CharField(max_length=255, null=True, blank=True)
    direction_ru = models.CharField(max_length=255, null=True, blank=True)
    direction_uz = models.CharField(max_length=255, null=True, blank=True)
    direction_en = models.CharField(max_length=255, null=True, blank=True)
    image = ResizedImageField(size=[600, 600], upload_to='expert/', null=True, blank=True)
    priority = models.IntegerField(default=1)

    class Meta:
        ordering = ('priority',)


###########################################################
# Office
###########################################################
class Office(models.Model):
    address_ru = models.CharField(max_length=500, null=True, blank=True)
    address_en = models.CharField(max_length=500, null=True, blank=True)
    address_uz = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    gmap = models.CharField(max_length=500, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    youtube = models.CharField(max_length=255, null=True, blank=True)
    telegram_bot = models.CharField(max_length=255, null=True, blank=True)

    #
    about_image = ResizedImageField(size=[1060, 800], upload_to='photos/', null=True, blank=True)


    def get_iframe(self):
        try: return self.gmap.split('"')[1]
        except: return ""

    def get_students_count(self):
        return Student.objects.all().count()

    def get_completed_students_count(self):
        c = 0
        for i in Student.objects.all():
            if i.status == "Сертификат тайёр" or i.completed:
                c+=1
        return c

    def get_registered_students_count(self):
        return Student.objects.filter(status="Сўровнома тўлдирилди").count()

    def get_registering_students_count(self):
        return Student.objects.filter(status="Рўйхатдан ўтмоқда").count()

    def get_experts_count(self):
        return Expert.objects.all().count()

    def get_districts_count(self):
        return District.objects.filter(available=True).count()


###########################################################
# Office Phone
###########################################################
class Phone(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)


###########################################################
# Office Email
###########################################################
class Email(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)


###########################################################
# Gallery
###########################################################
class Gallery(models.Model):
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    priority = models.IntegerField(default=1)

    def count_photos(self):
        return GalleryPhoto.objects.filter(folder_id = self.id).count()

    class Meta:
        ordering = ('priority',)


###########################################################
# Gallery Photo
###########################################################
class GalleryPhoto(models.Model):
    folder = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True, blank=True)
    image = ResizedImageField(size=[1920, 1200], upload_to='photos/', null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    priority = models.IntegerField(default=1)

    class Meta:
        ordering = ('priority',)


###########################################################
# Feedback
###########################################################
class FeedBack(models.Model):
    fio = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)


###########################################################
# Question for Experts
###########################################################
class QFE(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, null=True, blank=True)
    fio = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    answered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)


###########################################################
# Course
###########################################################
class Course(models.Model):
    title_ru = models.CharField(max_length=500, null=True, blank=True)
    title_uz = models.CharField(max_length=500, null=True, blank=True)
    title_en = models.CharField(max_length=500, null=True, blank=True)
    content_ru = models.TextField()
    content_uz = models.TextField()
    content_en = models.TextField()
    priority = models.IntegerField(default=1)
    image = ResizedImageField(size=[550, 550], upload_to='course/', null=True, blank=True)
    time_interval = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ('priority',)


###########################################################
# Region
###########################################################
class Region(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def districts_count(self):
        districts = District.objects.filter(available=True, region=self)
        return districts.count()


###########################################################
# District
###########################################################
class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


###########################################################
# Student
###########################################################

class FA(models.Model):
    code = models.CharField(max_length=255)
    count = models.IntegerField(default=0)


class Student(models.Model):
    fio = models.CharField(max_length=255, null=True, blank=True)
    inn = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    birthday = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=500, null=True, blank=True)
    activity = models.CharField(max_length=255, null=True, blank=True)
    job = models.CharField(max_length=255, null=True, blank=True)
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateField(null=True, blank=True)
    platform = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    certificate_id = models.CharField(max_length=255, null=True, blank=True)
    completed = models.BooleanField(default=False)
    pdf_created = models.BooleanField(default=False)
    tstatuses = [("start", "Ro'yxatdan o'tmoqda"), ("end", "Ro'yxatdan o'tgan")]
    tstatus = models.CharField(max_length=255, default="start", choices=tstatuses)
    tgenders = [("male", "Erkak"), ("female", "Ayol")]
    tgender = models.CharField(max_length=255, null=True, blank=True, choices=tgenders)
    file = models.FileField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Если tgender установлен, устанавливаем его значение в поле gender
        if self.tgender:
            self.gender = self.get_tgender_display()
        
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.fio} [{self.telegram_id}] ({self.phone if self.phone else 'Телефон киритилмаган'})"

    def date_created_custom(self):
        try:
            d = parser.parse(self.date_created.strftime("%Y-%m-%d %H:%M"))
            return (d + relativedelta(hours=+5)).strftime("%Y-%m-%d %H:%M")
        except: return ""

    def date_certificate(self):
        try: 
            if self.date_confirmed is None:
                return str(self.date_created.strftime('%d %m %Y'))
            return str(self.date_confirmed.strftime('%d %m %Y'))
        except: return ""

    class Meta:
        ordering = ('-date_created',)


###########################################################
# Captcha
###########################################################
class Captcha(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    image = ResizedImageField(size=[250, 100], upload_to='captchas/', null=True, blank=True)


###########################################################
# Account
###########################################################
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    districts = models.TextField()

    def __str__(self):
        return str(self.user.username)


###########################################################
# Excel
###########################################################
class Excel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    file = models.TextField(null=True, blank=True)
    download = models.BooleanField(default=False)

    class Meta:
        ordering=("download",)

    def __str__(self):
        return str(self.title)


###########################################################
# Book
###########################################################

class CategoryBook(models.Model):
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)

class Book(models.Model):
    category = models.ForeignKey(CategoryBook, on_delete=models.CASCADE)
    pdf = models.FileField(null=True, blank=True, upload_to="books/")
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_uz = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    priority = models.IntegerField(default=1)

    class Meta:
        ordering = ('priority',)



###########################################################
# Video
###########################################################

class Video(models.Model):
    title_ru = models.CharField(max_length=500, null=True, blank=True)
    title_uz = models.CharField(max_length=500, null=True, blank=True)
    title_en = models.CharField(max_length=500, null=True, blank=True)
    priority = models.IntegerField(default=1)
    image = ResizedImageField(size=[550, 550], upload_to='videos/', null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ('priority',)


###########################################################
# BranchForMap
###########################################################


class BranchForMap(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    lat = models.CharField(max_length=255)
    lon = models.CharField(max_length=255)

    def __str__(self):
        return self.title


###########################################################
# Calendar Program
###########################################################
class Program(models.Model):
    title_ru = models.CharField(max_length=500, null=True, blank=True)
    title_uz = models.CharField(max_length=500, null=True, blank=True)
    title_en = models.CharField(max_length=500, null=True, blank=True)
    content_ru = models.TextField()
    content_uz = models.TextField()
    content_en = models.TextField()
    date = models.DateField()

    class Meta:
        ordering = ('date',)