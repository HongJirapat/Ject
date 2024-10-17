from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authen/', include('authen.urls')),
    path('thread/', include('thread.urls')),
]
