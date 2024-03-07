from typing import Any
#django imports...
from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
#others....
from hr.forms import LoginForm,CategoryForm,JobForm,JobChangeForm
from myapp.models import Category,Jobs,Applications

from jobseeker.views import signin_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages


# Create your views here.

def admin_permission_required(fn):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request,"Admin Permission Required")
            return redirect("signin")
        else:
            return fn(request,*args, **kwargs)
    return wrapper

decs=(admin_permission_required,never_cache,signin_required)




class SiginView(FormView):
    template_name="signin.html"
    form_class=LoginForm
    
    def post(self,request,*args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print("successs")
                if request.user.is_superuser:
                    return redirect("indexhr")
                else:
                    return redirect("indexseeker")
        print("failed")
        return render(request,"signin.html",{"form":form})


@method_decorator(decs,name="dispatch")
class DashbordView(TemplateView):
    template_name="index.html"


@method_decorator(decs,name="dispatch")
class SignoutView(View):
    def get(self,request,*args, **kwargs):
        logout(request)
        return redirect("signin")


@method_decorator(decs,name="dispatch")
class CategoryView(CreateView,ListView):

    template_name="category.html"
    form_class=CategoryForm
    success_url=reverse_lazy("category")
    context_object_name="data"
    model=Category

#    def get(self,request,*args,**kwargs):
#         form=CategoryForm()
#         qs=Category.objects.all()
#         return render(request,"category.html",{"form":form, "data":qs})
   
#    def post(self,request,*args,**kwargs):
#        form=CategoryForm(request.POST)
#        if form.is_valid():
#            form.save()
#            print("category added")
#            return redirect("category")
#        else:
#            print("error")
#            return redirect("category")


@method_decorator(decs,name="dispatch")
class CategoryDeleteView(View):
   def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        print(id)
        qs=Category.objects.get(id=id).delete()
        return redirect('category')


@method_decorator(decs,name="dispatch")
class JobcreateView(CreateView):
    template_name="jobadd.html"
    form_class=JobForm
    success_url=reverse_lazy("listjob")

   
@method_decorator(decs,name="dispatch")
class JoblistView(ListView):
    template_name="listjob.html"
    context_object_name="data"
    model=Jobs
    
    def get(self,request,*args, **kwargs):
        qs=Jobs.objects.all()

        if "status" in request.GET:
            value=request.GET.get("status")
            qs=qs.filter(status=value)
        return render(request,"listjob.html",{"data":qs})
    

    # def get_queryset(self):
    #     return Jobs.objects.filter(status=True)

    # def get(self,request,*args, **kwargs):
    #     qs=Jobs.objects.all()
    #     return render(request,"listjob.html",{"data":qs})


@method_decorator(decs,name="dispatch")
class JobdeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        print(id)
        qs=Jobs.objects.get(id=id).delete()
        return redirect('listjob')


@method_decorator(decs,name="dispatch")
class JobUpdateView(UpdateView):
    form_class=JobChangeForm
    template_name="jobedit.html"
    model=Jobs
    success_url=reverse_lazy("listjob")



#localhost:8000/jobs/<int:pk>/application
    
@method_decorator(decs,name="dispatch")
class JobApplicationView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        job_obj=Jobs.objects.get(id=id)
        qs=Applications.objects.filter(job=job_obj)
        return render(request,"applicationhr.html",{"data":qs})


@method_decorator(decs,name="dispatch")
class ApplicationDetailView(DetailView):
    template_name="applicationdetails.html"
    context_object_name="application"
    model=Applications

    def get_context_data(self, **kwargs: Any) :
        context=super().get_context_data(**kwargs)
        print(context)
        return context


@method_decorator(decs,name="dispatch")
class ApplicationUpdateView(View):

    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        Applications_object=Applications.objects.get(id=id)
        applicant_mails=Applications_object.student.email
        value=request.POST.get("status")
        Applications.objects.filter(id=id).update(status=value)
        if value=="shortlisted":
            send_mail("your appliction status has been changed",
                  "your appliction status changed",
                  "arjunkbabu2001sep3@gmail.com",
                  ["abhilashabhivkm686143upm@gmail.com"],
                  fail_silently=False)
        return redirect("indexhr")