from django.urls import path
from . import views


urlpatterns = [
    # Auth urls
    path('', views.login_index, name='login_index'),
    path('logout/', views.login_logout, name='login_logout'),


    # Reset urls
    path('reset/', views.login_reset, name='login_reset'),
        path('reset/sent/', views.login_reset_send_code, name='login_reset_send_code'),
        path('reset/complete/', views.login_reset_complete, name='login_reset_complete'),
]