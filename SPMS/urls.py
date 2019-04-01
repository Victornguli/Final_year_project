from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", ViewPastProjects , name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", SignUp, name="select_signup"),
    path("accounts/signup/student/", StudentSignUp.as_view(), name = "student_signup" ),
    path("accounts/signup/supervisor/", SupervisorSignUp.as_view(), name = "supervisor_signup"),

    path("appointments/request_appointment", RequestAppointment , name="request_appointment"),
    path("appointments/update_timeslots", SelectAvailableDays , name="select_days"),
    path("appointments/delete_timeslots(<availableday_id>[0-9]+)(<day>[a-z]+)", DeleteAvailableDays , name="delete_timeslot"),
    path("appointments/save_days", SaveAvailableDays , name="save_days"),
    path("appointments/view_appointments", ViewAppointments , name="appointments"),
    path("appointments/approved_appointments", view_approved_appointments , name="approved_appointments"),
    path("appointments/view_available_slots", ViewAvailableDays , name="view_available"),
    path("appointments/approve_appointment(<appointment_id>[0-9]+)",ApproveAppointment, name="approve_appointment"),
    path("appointments/reject_appointment(<appointment_id>[0-9]+)", RejectAppointment , name="reject_appointment"),

    path("coordinator/set_schedule", SetSchedule , name="set_schedule"),
    path("coordinator/set_milestone", SetMilestones , name="set_milestone"),

    path("student/profile", ViewProfile , name="student_view_profile"),
    path("student/profile/update_profile", UpdateProfile , name="student_update_profile"),
    path("student/project/create_project",createproject_view, name="create_project"),
    path("student/project", StudentProject , name="student_project"),

    path("supervisor/profile", ViewProfile , name="supervisor_view_profile"),
    path("supervisor/profile/update_profile", UpdateProfile, name="supervisor_update_profile"),

    path("student/project/upload_document(<milestone_id>[0-9]+)", upload_file, name="upload_document"),
    path("project/download(<document_id>[0-9]+)", download_document , name="download"),
    path("project/download_abstract(<abstract_id>[0-9]+)", download_abstract , name="download_abstract"),
    path("project/view_comments(<milestone_id>[0-9]+)(<student_id>[0-9]+)", view_comment , name="view_comments"),
    path('project/project_schedule', chart_view , name = 'project_schedule'),
    path("supervisor/project", project_view , name="project"),
    path("supervisor/project_supervision(<student_id>[0-9]+)", project_supervision_view , name="project_supervision"),
    path("supervisor/project_supervision/close_milestone(<milestone_id>[0-9]+)(<project_id>[0-9]+)", CloseMilestone , name="close_milestone"),
    path("supervisor/project_supervision/close_project(<project_id>[0-9]+)", CloseProject , name="close_project"),
    
    path("view_notifications", view_notifications, name="view_notifications"),
    #path('inbox/notifications/', include(notifications.urls, namespace='notifications')),    
    # path("past-projects/", PastProjets, name="projects"),
    # path("accounts/login",include("django.auth.urls")),

]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)