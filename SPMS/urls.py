"""SPMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Index, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", SignUp, name="select-signup"),
    path("accounts/signup/student/", StudentSignUp.as_view(), name = "student_signup" ),
    path("accounts/signup/supervisor/", SupervisorSignUp.as_view(), name = "supervisor_signup"),
    path("appointments/request_appointment", RequestAppointment , name="request_appointment"),
    path("appointments/select_days", SelectAvailableDays , name="select_days"),
    path("appointments/view_appointments", ViewAppointments , name="appointments"),
    path("appointments/approve_appointment(<appointment_id>[0-9]+)",ApproveAppointment, name="approve_appointment"),
    path("appointments/reject_appointment(<appointment_id>[0-9]+)", RejectAppointment , name="reject_appointment"),

    # path("past-projects/", PastProjets, name="projects"),
    # path("accounts/login",include("django.auth.urls")),

]

urlpatterns += staticfiles_urlpatterns()