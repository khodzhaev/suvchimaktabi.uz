from django.contrib import admin
from .models import *


class SetStudent(admin.ModelAdmin):
    search_fields = ["fio", "phone"]
    list_display = ("fio", "phone", "gender", "date_created")
    list_filter = ("region", "district")
admin.site.register(Student, SetStudent)

admin.site.register(Region)

admin.site.register(FA)

class SetDistrict(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("id", "title", "region")
    list_filter = ("region",)
admin.site.register(District, SetDistrict)

admin.site.register(QFE)

class SetAccount(admin.ModelAdmin):
    search_fields = ["districts"]
    list_display = ("user", "districts")
    list_filter = ("user",)
admin.site.register(Account, SetAccount)

class SetCaptcha(admin.ModelAdmin):
    list_display = ("code", "answer")
    search_fields = ["code", "answer"]
admin.site.register(Captcha, SetCaptcha)

class SetExcel(admin.ModelAdmin):
    list_display = ("user", "title", "file", "district", "download")
    search_fields = ["title", "file"]
    list_filter = ("user", "download")
admin.site.register(Excel, SetExcel)

admin.site.register(CategoryBook)
admin.site.register(BranchForMap)
admin.site.register(Office)
admin.site.register(Program)