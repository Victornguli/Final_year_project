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
    status = models.BooleanField(default=True)

class AvailableDay(models.Model):
    monday = models.TimeField(null=True)
    tuesday = models.TimeField(null=True)
    wednesday = models.TimeField(null=True)
    thursday = models.TimeField(null=True)
    friday = models.TimeField(null=True)
    saturday = models.TimeField(null=True)
    sunday = models.TimeField(null=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True)


class Appointment(models.Model):
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)

    Approved = "Approved"
    Applied = "Applied"

    status = (
        (Approved,"Approved"),
        (Applied,"Applied"),
    )
    approved = models.CharField(max_length = 10 , choices=status, default="Applied")

class Schedule(models.Model):
    start_date = models.DateField(auto_now_add=False, auto_now=False)
    end_date = models.DateField(auto_now_add=False, auto_now=False)

class Milestone(models.Model):
    Not_Started = "NS"
    Ongoing = "ON"
    Finished = "FN"

    milestone_status = (
        (Not_Started, "Not Started"),
        (Ongoing, "Ongoing"),
        (Finished, "Finished"),
    )

    milestone = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=False, auto_now=False)
    end_date = models.DateField(auto_now_add=False, auto_now=False)
    status = models.CharField(max_length=2, choices=milestone_status)


