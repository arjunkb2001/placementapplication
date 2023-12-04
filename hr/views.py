#django imports...
from django.shortcuts import render
from django.views.generic import *

#others....
from hr.forms import LoginForm
# Create your views here.

class SiginView(FormView):
    template_name="signin.html"
    form_class=LoginForm

    # def  get(self,request,*args, **kwargs):
    #     form=LoginForm
    #     return render(request,"signin.html",{"form":form})
    