from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path('index', index,name="Web Index"),
]
