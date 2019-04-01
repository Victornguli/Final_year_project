from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = "Student Project Management System";
admin.site.site_title = "SPMS Admin";
admin.site.index_title = "Project Coordination"

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_date', 'schedule', 'abstract']
    list_filter = ["schedule", "start_date","status"]

class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "course", "reg_number", "supervisor", "project", "status"]
    list_filter = ["course", "project","status"]

class MilestoneAdmin(admin.ModelAdmin):
    list_display = ["milestone_name", "start_date", "end_date", "schedule", "required_document", "semester"]
    list_filter = ["semester", "schedule", "start_date", "end_date"]

class PastProjectAdmin(admin.ModelAdmin):
    list_display = ["project"]
    list_filter = ["project"]

class SupervisorAdmin(admin.ModelAdmin):
    list_display = ["user","first_name", "last_name", "email"]

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["schedule_name", "start_date", "end_date", "status"]
    list_filter = ["start_date", "end_date" ,"status"]

class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "is_student",  "is_supervisor", "is_superuser", "is_staff"]
    list_filter = ["is_student", "is_supervisor"]

class AvailableDayAdmin(admin.ModelAdmin):
    list_display = ["supervisor", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    list_filter = ["supervisor"]

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["supervisor","student", "date", "time", "approved"]
    list_filter = ["supervisor","date","approved"]

class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "document", "upladed_at", "student", "milestone"]
    list_filter = ["student","milestone"]

class GroupAdmin(admin.ModelAdmin):
    list_display = ["semester", "start_date", "end_date"]
    list_filter = ["semester"]

class NotificationAdmin(admin.ModelAdmin):
    list_display = ["title", "text", "receiver","sent_time", "sent_date", "document"]
    list_filter = ["receiver", "sent_date"]

admin.site.register(Project, ProjectAdmin)
admin.site.register(PastProject, PastProjectAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(AvailableDay, AvailableDayAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Notification, NotificationAdmin)