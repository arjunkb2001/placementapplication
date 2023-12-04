#django imports...
from django.shortcuts import render
from django.views.generic import View

#others....
from hr.forms import LoginForm
# Create your views here.

class SiginView(View):
    def  get(self,request,*args, **kwargs):
        form=LoginForm
        return render(request,"login.html",{"form":form})