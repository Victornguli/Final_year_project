import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# import weekday_field

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=50,default="title")
    status = models.BooleanField(default = True)
    start_date = models.DateField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title


class PastProjects(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)


class User(AbstractUser):
    is_student = models.BooleanField("student_status",default=False)
    is_supervisor = models.BooleanField("supervisor_status",default=False)


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=255,  default="")


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=255,  default="")
    course = models.CharField(max_length=30, default="")
    reg_number = models.CharField(max_length=30, unique=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, null=True)


class Appointment(models.Model):
    supervisor = models.OneToOneField(Supervisor, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    approve = models.BooleanField(default = False)
    reject = models.BooleanField(default = False)


class AvailableDays(models.Model):
    DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
    )

    days = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    # weekdays = weekday_field.fields.WeekdayField()


