from django.urls import path
from django.contrib import admin
from AppStats.scheduler import execute
from AppStats.views import dashboard, load_appData


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', dashboard, name='apps'),
    path('data/<str:application>', load_appData, name='load'),
]

execute()