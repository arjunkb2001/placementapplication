#django imports...
from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
#others....
from hr.forms import LoginForm,CategoryForm,JobForm,JobChangeForm
from myapp.models import Category,Jobs


# Create your views here.

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

class DashbordView(TemplateView):
    template_name="index.html"

class SignoutView(View):
    def get(self,request,*args, **kwargs):
        logout(request)
        return redirect("signin")
    
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



class CategoryDeleteView(View):
   def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        print(id)
        qs=Category.objects.get(id=id).delete()
        return redirect('category')
   
class JobcreateView(CreateView):
    template_name="jobadd.html"
    form_class=JobForm
    success_url=reverse_lazy("listjob")
    

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


class JobdeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        print(id)
        qs=Jobs.objects.get(id=id).delete()
        return redirect('listjob')

class JobUpdateView(UpdateView):
    form_class=JobChangeForm
    template_name="jobedit.html"
    model=Jobs
    success_url=reverse_lazy("listjob")


   