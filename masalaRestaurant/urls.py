from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
admin.site.site_title = 'Masala Uganda'
admin.site.index_title = 'Welcome to Masala Uganda Admin Panel'
admin.site.site_header = 'Masala Uganda'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('mainApp.urls') ),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)