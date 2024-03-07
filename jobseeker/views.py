from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from django.views.generic import View,CreateView,TemplateView,DetailView,UpdateView,ListView

from jobseeker.forms import RegistrationForm,ProfileForm
from myapp.models import StudentProfile,Jobs,Applications,Category

# Create your views here.


# DECRATORS ---->

def signin_required(fn):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args, **kwargs)
    return wrapper

decs=[never_cache,signin_required]


class SignUpView(CreateView):
    template_name="jobseeker/register.html"
    form_class = RegistrationForm
    success_url=reverse_lazy("signin")

@method_decorator(decs,name="dispatch")
class SignoutView(View):
    def get(self,request,*args, **kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(decs,name="dispatch")
class StudentIndexView(ListView):
    template_name="jobseeker/index.html"
    context_object_name="data"
    model=Jobs
    # def get_queryset(self):
    #     qs=Jobs.objects.all().order_by("-created_date")
    #     return qs
    
    def get_queryset(self):
        my_application=Applications.objects.filter(student=self.request.user).values_list("job",flat=True)
        # id .....
        qs=Jobs.objects.exclude(id__in=my_application).order_by("-created_date")
        
        # localhost:8000/seeker/index/?category=frontent
        
        if "category" in self.request.GET:
            category_value=self.request.GET.get("category")
            print(category_value)
            qs=qs.filter(category__name=category_value)
        return qs
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        qs=Category.objects.all()
        print(qs)
        context["categories"]=qs
        return context
    
@method_decorator(decs,name="dispatch")
class ProfileCreateView(CreateView):

    template_name="jobseeker/profile.html"
    form_class=ProfileForm
    success_url=reverse_lazy("indexseeker")

    def form_valid(self, form):
        form.instance.user=self.request.user

        return super().form_valid(form)
    
@method_decorator(decs,name="dispatch")
class ProfileDetailView(DetailView):
     
     template_name="jobseeker/detailprofile.html"
     context_object_name="data"

     model=StudentProfile

@method_decorator(decs,name="dispatch")
class ProfileEditView(UpdateView):
    template_name="jobseeker/profileedit.html"
    form_class=ProfileForm
    model=StudentProfile
    success_url=reverse_lazy("indexseeker")

# class JoblistView(ListView):
#     template_name="jobseeker/joblist.html"
#     context_object_name="data"
#     model=Jobs

# seeker/jobs/<int:pk>/detail
    
@method_decorator(decs,name="dispatch")
class JobDetailView(DetailView):
    
    template_name="jobseeker/jobdetail.html"
    model=Jobs
    context_object_name="data"

# seeker/jobs/<int:pk>/apply
@method_decorator(decs,name="dispatch")
class ApplyJobView(View):
    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        job_object=Jobs.objects.get(id=id)
        student_object=request.user
        Applications.objects.create(job =job_object,student=student_object)
        return redirect("indexseeker")

@method_decorator(decs,name="dispatch")
class ApplicationListView(ListView):
    template_name="jobseeker/applications.html"
    model=Applications
    context_object_name="data"

    def get_queryset(self):
        qs=Applications.objects.filter(student=self.request.user)
        print(qs)
        return qs

# localhost:8000/job/<int:pk>/save
@method_decorator(decs,name="dispatch")
class JobSaveView(View):
    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        job_object=Jobs.objects.get(id=id)
        action=request.POST.get("action") #save/unsave
        if action=="save":
            request.user.profile.saved_jobs.add(job_object)
        elif action=="unsave":
            request.user.profile.saved_jobs.remove(job_object)
        return redirect("indexseeker")

@method_decorator(decs,name="dispatch")
class SavedJobView(View):
    template_name="jobseeker/savedjob.html"
    model=StudentProfile
    def get(self,request,*args, **kwargs):
        qs=request.user.profile.saved_jobs.all()
        return render(request,self.template_name,{"data":qs})