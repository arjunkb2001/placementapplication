from django.urls import path
from myapp.views import *

urlpatterns = [
    path("",SiginView.as_view(),name="login")
]