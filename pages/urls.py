from django.urls import path
from . import views


urlpatterns = [
    path('', views.pages_index, name="pages_index"),
        path('qfe/', views.pages_qfe_create),
        path('register/', views.pages_register),
        path('phone/check/', views.pages_phone_check),
        path('inn/check/', views.pages_inn_check),
        path('regions/', views.pages_regions),
        path('certificate/download/', views.pages_certificate_download),

    path('about/', views.pages_about, name="pages_about"),

    path('experts/', views.pages_qfe, name="pages_qfe"),

    path('course/', views.pages_course, name="pages_course"),
    path('course/fermer/', views.pages_course_fermer, name="pages_course_fermer"),
    path('course/loyihachi/', views.pages_course_loyihachi, name="pages_course_loyihachi"),

    path('news/', views.pages_news_all, name="pages_news_all"),
    path('news/<int:id>/', views.pages_news_detail, name="pages_news_detail"),

    path('videos/', views.pages_videos, name="pages_videos"),

    path('gallery/', views.pages_gallery_all, name="pages_gallery_all"),
    path('gallery/<int:id>/', views.pages_gallery_detail, name="pages_gallery_detail"),

    path('books_category/', views.pages_books_category, name="pages_books_category"),
    path('books/<int:category_id>/', views.pages_books, name="pages_books"),

    path('contact/', views.pages_contact, name="pages_contact"),
        path('feedback/', views.pages_feedback_create),
        path('captcha/', views.pages_captcha_refresh),



    path('programs/calendar/', views.programs_calendar, name='programs_calendar'),
]