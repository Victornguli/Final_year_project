
from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

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
    path("coordinator/set_schedule", SetSchedule , name="set_schedule"),
    path("coordinator/set_milestone", SetMilestones , name="set_milestone"),
    path("student/update_profile", UpdateProfile , name="update_profile"),
    path("student/project", StudentProject , name="student_project"),
    path("supervisor/update_profile", UpdateProfile , name="update_profile"),

    # path("past-projects/", PastProjets, name="projects"),
    # path("accounts/login",include("django.auth.urls")),

]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)