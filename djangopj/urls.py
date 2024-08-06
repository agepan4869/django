# djangopj/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from top import views as top_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('file/', include('file_downloader.urls')),
    path('', top_views.top_page, name='top_page'),  # URLパターンを渡す
    path('test/', include('test_output.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
