from django.urls import path
from hr.views import *

urlpatterns = [
    path("signin",SiginView.as_view(),name="login")
]