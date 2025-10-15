from django.contrib import admin
from django.urls import path
from api.views import registrationForm,homepage,logout,login
# for static,media files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/',registrationForm,name='reg'),
    path('home/',homepage,name='home'),
    path('logout/',logout,name='logout'),
    path('login/',login,name='login')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
