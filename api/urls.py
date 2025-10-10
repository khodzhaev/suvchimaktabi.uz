from django.urls import path, include
from . import views

app_name= "api"

urlpatterns = [
    path("user/", views.user),
    path("answer/", views.answer)
]