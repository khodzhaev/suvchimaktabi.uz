from django.urls import path
from . import views


urlpatterns = [
    # index urls
    path('', views.control_index, name='control_index'),
        path('office/edit/', views.control_index_office_edit, name='control_index_office_edit'),
        path('office/phone/create/', views.control_index_phone_create, name='control_index_phone_create'),
        path('office/phone/remove/', views.control_index_phone_remove, name='control_index_phone_remove'),
        path('office/email/create/', views.control_index_email_create, name='control_index_email_create'),
        path('office/email/remove/', views.control_index_email_remove, name='control_index_email_remove'),


    # Gallery urls
    path('gallery/', views.control_gallery, name='control_folder'),
    path('gallery/add/', views.control_gallery_add, name='control_folder_add'),
    path('gallery/<int:id>/', views.control_gallery_detail, name='control_folder_detail'),
        path('gallery/folder/create/', views.control_gallery_create, name='control_folder_create'),
        path('gallery/folder/edit/', views.control_gallery_edit, name='control_folder_edit'),
        path('gallery/folder/remove/', views.control_gallery_remove, name='control_folder_remove'),

        # Gallery photo urls
        path('gallery/create/', views.control_gallery_photo_create, name='control_gallery_create'),
        path('gallery/edit/', views.control_gallery_photo_edit, name='control_gallery_edit'),
        path('gallery/remove/', views.control_gallery_photo_remove, name='control_gallery_remove'),


    # News urls
    path('news/', views.control_news, name='control_news'),
    path('news/add/', views.control_news_add, name='control_news_add'),
    path('news/<int:id>/', views.control_news_detail, name='control_news_detail'),
        path('news/create/', views.control_news_create, name='control_news_create'),
        path('news/edit/', views.control_news_edit, name='control_news_edit'),
        path('news/remove/', views.control_news_remove, name='control_news_remove'),


    # Course urls
    path('course/', views.control_course, name='control_course'),
    path('course/add/', views.control_course_add, name='control_course_add'),
    path('course/<int:id>/', views.control_course_detail, name='control_course_detail'),
        path('course/create/', views.control_course_create, name='control_course_create'),
        path('course/edit/', views.control_course_edit, name='control_course_edit'),
        path('course/remove/', views.control_course_remove, name='control_course_remove'),


    # Staff urls
    path('staff/', views.control_staff, name='control_staff'),
    path('staff/add/', views.control_staff_add, name='control_staff_add'),
    path('staff/<int:id>/', views.control_staff_detail, name='control_staff_detail'),
        path('staff/create/', views.control_staff_create, name='control_staff_create'),
        path('staff/edit/', views.control_staff_edit, name='control_staff_edit'),
        path('staff/remove/', views.control_staff_remove, name='control_staff_remove'),


    # Expert urls
    path('expert/', views.control_expert, name='control_expert'),
    path('expert/add/', views.control_expert_add, name='control_expert_add'),
    path('expert/<int:id>/', views.control_expert_detail, name='control_expert_detail'),
        path('expert/create/', views.control_expert_create, name='control_expert_create'),
        path('expert/edit/', views.control_expert_edit, name='control_expert_edit'),
        path('expert/remove/', views.control_expert_remove, name='control_expert_remove'),


    # Testimonial urls
    path('testi/', views.control_testi, name='control_testi'),
    path('testi/add/', views.control_testi_add, name='control_testi_add'),
    path('testi/<int:id>/', views.control_testi_detail, name='control_testi_detail'),
        path('testi/create/', views.control_testi_create, name='control_testi_create'),
        path('testi/edit/', views.control_testi_edit, name='control_testi_edit'),
        path('testi/remove/', views.control_testi_remove, name='control_testi_remove'),


    # QA urls
    path('qa/', views.control_qa, name='control_qa'),
    path('qa/add/', views.control_qa_add, name='control_qa_add'),
    path('qa/<int:id>/', views.control_qa_detail, name='control_qa_detail'),
        path('qa/create/', views.control_qa_create, name='control_qa_create'),
        path('qa/edit/', views.control_qa_edit, name='control_qa_edit'),
        path('qa/remove/', views.control_qa_remove, name='control_qa_remove'),


    # FeedBack urls
    path('feedback/', views.control_feedback, name='control_feedback'),
        path('feedback/remove/', views.control_feedback_remove, name='control_feedback_remove'),


    # User urls
    path('users/', views.control_users, name='control_users'),
    path('users/add/', views.control_users_add, name='control_users_add'),
    path('users/<int:id>/', views.control_users_detail, name='control_users_detail'),
        path('users/create/', views.control_users_create, name='control_users_create'),
        path('users/edit/', views.control_users_edit, name='control_users_edit'),
        path('users/remove/', views.control_users_remove, name='control_users_remove'),

        # User district api
        path('users/districts/', views.control_user_districts_api, name='control_user_districts_api'),


    # Region urls
    path('region/', views.control_region, name='control_region'),
    path('region/add/', views.control_region_add, name='control_region_add'),
    path('region/<int:id>/', views.control_region_detail, name='control_region_detail'),
        path('region/create/', views.control_region_create, name='control_region_create'),
        path('region/edit/', views.control_region_edit, name='control_region_edit'),
        path('region/remove/', views.control_region_remove, name='control_region_remove'),


    # District urls
    path('district/', views.control_district, name='control_district'),
    path('district/add/', views.control_district_add, name='control_district_add'),
    path('district/<int:id>/', views.control_district_detail, name='control_district_detail'),
        path('district/create/', views.control_district_create, name='control_district_create'),
        path('district/edit/', views.control_district_edit, name='control_district_edit'),
        path('district/remove/', views.control_district_remove, name='control_district_remove'),


    # Student urls
    path("students/", views.control_students, name='control_students'),
        path("students/status_change/", views.control_students_status_change, name='control_students_status_change'),
        path("students/delete/", views.control_students_delete, name='control_students_delete'),
        path("students/edit/", views.control_students_edit, name='control_students_edit'),
        path("students/certificate/", views.control_students_certificate, name='control_students_certificate'),
        path("students/sms/send/", views.control_students_sms_send, name='control_students_sms_send'),
        path("students/excel/", views.control_students_excel, name='control_students_excel'),


    # QFE urls
    path('qfe/', views.control_qfe, name='control_qfe'),
        path('qfe/remove/', views.control_qfe_remove, name='control_qfe_remove'),


    # Excel urls
    path('excel/', views.control_excel, name='control_excel'),
        path('excel/remove/', views.control_excel_remove, name='control_excel_remove'),
        path('excel/create/', views.control_excel_create, name='control_excel_create'),
        # path('excel/umumiy/', views.control_excel_umumiy, name='control_excel_umumiy'),


    # Book urls
    path('book/', views.control_book, name='control_book'),
    path('book/add/', views.control_book_add, name='control_book_add'),
    path('book/<int:id>/', views.control_book_detail, name='control_book_detail'),
        path('book/create/', views.control_book_create, name='control_book_create'),
        path('book/edit/', views.control_book_edit, name='control_book_edit'),
        path('book/remove/', views.control_book_remove, name='control_book_remove'),


    # Video urls
    path('video/', views.control_video, name='control_video'),
    path('video/add/', views.control_video_add, name='control_video_add'),
    path('video/<int:id>/', views.control_video_detail, name='control_video_detail'),
        path('video/create/', views.control_video_create, name='control_video_create'),
        path('video/edit/', views.control_video_edit, name='control_video_edit'),
        path('video/remove/', views.control_video_remove, name='control_video_remove'),


    # Program urls
    path('program/', views.control_program, name='control_program'),
    path('program/add/', views.control_program_add, name='control_program_add'),
    path('program/<int:id>/', views.control_program_detail, name='control_program_detail'),
        path('program/create/', views.control_program_create, name='control_program_create'),
        path('program/edit/', views.control_program_edit, name='control_program_edit'),
        path('program/remove/', views.control_program_remove, name='control_program_remove'),
]