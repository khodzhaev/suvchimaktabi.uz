from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400

from control.views import certificate_view, certificate_view_a

urlpatterns = [
    path('', include('pages.urls')),
    path('certificate/<str:certificate_code>/', certificate_view),
    path('certificate_/<str:certificate_code>/', certificate_view_a),
    path('login/', include('login.urls')),
    path('control/', include('control.urls')),
    path("api/", include("api.urls")),
    path('__admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "pages.views.pages_404"
