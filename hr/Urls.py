from django.urls import path
from hr.views import *

urlpatterns = [
    path("",SiginView.as_view(),name="signin"),
    path("index",DashbordView.as_view(),name="indexhr"),
    path("logout",SignoutView.as_view(),name="signout"),
    path("category",CategoryView.as_view(),name="category"),
    path('remove/<int:pk>',CategoryDeleteView.as_view(),name="delete"),
    path("addjob",JobcreateView.as_view(),name="addjob"),
    path("listjob",JoblistView.as_view(),name="listjob"),
    path("editjob/<int:pk>",JobUpdateView.as_view(),name="editjob"),
    path('removejob/<int:pk>',JobdeleteView.as_view(),name="deletejob"),
    path('job/<int:pk>/application',JobApplicationView.as_view(),name="applicationlist"),
    path('application/<int:pk>',ApplicationDetailView.as_view(),name="applicationdetails"),
    path('application/<int:pk>/status',ApplicationUpdateView.as_view(),name="applicationstatus"),
]