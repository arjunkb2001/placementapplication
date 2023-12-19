from django.urls import path

from jobseeker.views import *

urlpatterns = [
    path("register/",SignUpView.as_view(),name="signup"),
    path("index/",StudentIndexView.as_view(),name="indexseeker"),
    path("addprofile/",ProfileCreateView.as_view(),name="profile"),
    path("detail/<int:pk>/profile/",ProfileDetailView.as_view(),name="profiledetail"),
    path("profile/<int:pk>/change",ProfileEditView.as_view(),name="profileedit"),
    path("signout/seeker",SignoutView.as_view(),name="logout"),
    path("job/<int:pk>/detail",JobDetailView.as_view(),name="detailjob"),
    path("job/<int:pk>/apply",ApplyJobView.as_view(),name="applyjob"),
]

