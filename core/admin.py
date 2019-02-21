from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(PastProject)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Milestone)
admin.site.register(Schedule)
admin.site.register(AvailableDay)