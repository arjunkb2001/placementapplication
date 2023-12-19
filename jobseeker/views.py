from django.forms.models import BaseModelForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from django.views.generic import View,CreateView,TemplateView,DetailView,UpdateView,ListView

from jobseeker.forms import RegistrationForm,ProfileForm
from myapp.models import StudentProfile,Jobs,Applications

# Create your views here.

class SignUpView(CreateView):
    template_name="jobseeker/register.html"
    form_class = RegistrationForm
    success_url=reverse_lazy("signin")

class SignoutView(View):
    def get(self,request,*args, **kwargs):
        logout(request)
        return redirect("signin")


class StudentIndexView(ListView):
    template_name="jobseeker/index.html"
    context_object_name="data"
    model=Jobs
    def get_queryset(self):
        qs=Jobs.objects.all().order_by("-created_date")
        return qs
    

class ProfileCreateView(CreateView):

    template_name="jobseeker/profile.html"
    form_class=ProfileForm
    success_url=reverse_lazy("indexseeker")

    def form_valid(self, form):
        form.instance.user=self.request.user

        return super().form_valid(form)
    
class ProfileDetailView(DetailView):
     
     template_name="jobseeker/detailprofile.html"
     context_object_name="data"

     model=StudentProfile

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
class JobDetailView(DetailView):
    
    template_name="jobseeker/jobdetail.html"
    model=Jobs
    context_object_name="data"

# seeker/jobs/<int:pk>/apply
    
class ApplyJobView(View):
    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        job_object=Jobs.objects.get(id=id)
        student_object=request.user
        Applications.objects.create(jobs=job_object,student=student_object)
        return redirect("indexseeker")