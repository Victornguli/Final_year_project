import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class Schedule(models.Model):
    schedule_name = models.CharField(max_length = 100, default="")
    start_date = models.DateField(auto_now_add=False, auto_now=False)
    end_date = models.DateField(auto_now_add=False, auto_now=False)
    status = models.BooleanField(default=1)

    def __str__(self):
        return self.schedule_name

class Project(models.Model):
    title = models.CharField(max_length=50,default="title")
    status = models.BooleanField(default = True)
    start_date = models.DateField(auto_now=False, auto_now_add=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class PastProject(models.Model):
    past_project = models.ForeignKey(Project, on_delete=models.CASCADE)

class User(AbstractUser):
    is_student = models.BooleanField("student_status",default=False)
    is_supervisor = models.BooleanField("supervisor_status",default=False)


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=255,  default="")

    def __str__(self):
        return self.first_name + " " + self.last_name   


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

    def __str__(self):
        return self.first_name + " " + self.last_name

class AvailableDay(models.Model):
    monday = models.TimeField(null=True)
    tuesday = models.TimeField(null=True)
    wednesday = models.TimeField(null=True)
    thursday = models.TimeField(null=True)
    friday = models.TimeField(null=True)
    saturday = models.TimeField(null=True)
    sunday = models.TimeField(null=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.supervisor.first_name + " " + self.supervisor.last_name



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


class Milestone(models.Model):
    Not_Started = "NS"
    Ongoing = "ON"
    Finished = "FN"
    first_semester = "S1"
    second_semester = "S2"

    milestone_group = (
        (first_semester, "Semester One"),
        (second_semester, "Semester Two"),
    )

    milestone_status = (
        (Not_Started, "Not Started"),
        (Ongoing, "Ongoing"),
        (Finished, "Finished"),
    )

    milestone_name = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=False, auto_now=False)
    end_date = models.DateField(auto_now_add=False, auto_now=False)
    status = models.CharField(max_length=2, choices=milestone_status, default="NS")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    required_document = models.CharField(max_length=100, null=True)
    group = models.CharField(choices=milestone_group, default = "S1", max_length=2)

    def __str__(self):
        return self.milestone_name  

class Document(models.Model):
    title = models.CharField(max_length=50)
    document = models.FileField(upload_to="")
    upladed_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=200)
    student = models.ForeignKey(Student, null=False, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, null=False, on_delete=models.CASCADE)
    sender = models.BooleanField(default=0)
    sent_date = models.DateField(auto_now_add=False, auto_now=True)
    milestone = models.ForeignKey(Milestone, null=False, on_delete=models.CASCADE)

