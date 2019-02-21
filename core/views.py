from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import *

def SignUp(request):
    return render(request, "registration/signup.html")

class StudentSignUp(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def Index(request):
    form = UserCreationForm()
    return render(request, "core/index.html", {"form":form})


class SupervisorSignUp(CreateView):
    model = User
    form_class = SupervisorSignUpForm
    template_name = "registration/signup_form.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = 'supervisor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")

# def Login(request):
#     if request.method == "POST":
#         form = UserCreationForm()
#         if form.is_valid:
#             login(request, user)
#             return redirect(request, login)
#     return render(request, "core/base.html")

# def PastProjets(request):
#     return render(request, "core/projects.html")

def RequestAppointment(request):
    form = CreateAppointmentForm(request.POST) 
    user = request.user
    supervisor = user.student.supervisor  
    available_days = AvailableDay.objects.filter(supervisor_id = supervisor.id)
    if form.is_valid():  
        date = form.cleaned_data.get("date")
        time = form.cleaned_data.get("time")
        appointment = Appointment.objects.create(date=date, time=time, student_id= user.student.id, supervisor_id = supervisor.id)
        return render(request, 'core/request_appointment.html',{"form":form, "available_days":available_days, "supervisor":supervisor})

    
    return render(request,'core/request_appointment.html',{"form":form, "available_days":available_days, "supervisor":supervisor})
        # return render(request, "core/request-appointment.html")

def SelectAvailableDays(request):
    form =  SelectAvailableDaysForm(request.POST)
    user = request.user
    exists = AvailableDay.objects.filter(supervisor_id = user.supervisor).count()
    print (exists)
    if form.is_valid():
        monday = form.cleaned_data.get("monday")
        tuesday = form.cleaned_data.get("tuesday")
        wednesday = form.cleaned_data.get("wednesday")
        thursday = form.cleaned_data.get("thursday")
        friday = form.cleaned_data.get("friday")
        saturday = form.cleaned_data.get("saturday")
        sunday = form.cleaned_data.get("sunday")
        supervisor = user.supervisor

        if exists < 1:
            available_day = AvailableDay.objects.create(monday=monday, tuesday=tuesday, wednesday=wednesday, thursday=thursday, friday=friday, saturday=saturday, sunday=sunday,supervisor=supervisor)
        else:
            pass

        return render(request, "core/select_available.html" , {"form2":form})
    return render(request, "core/select_available.html" , {"form2":form})    


def ViewAvailableDays(request):
    days = AvailableDay.objects.all()
    appointments = Appointment.objects.all()
    students = Student.objects.all()
    return render(request, "core/request_appointment.html" , {"days":days, "appointments":appointments, "students":students })   


def ViewAppointments(request):
    days = AvailableDay.objects.all()
    appointments = Appointment.objects.all()
    students = Student.objects.all() 
    return render(request, "core/appointments.html" , {"days":days, "appointments":appointments, "students":students })     

def ApproveAppointment(request, appointment_id):
    appointment = Appointment.objects.get(pk = appointment_id)
    appointment.approved = "Approved"
    appointment.save()
    return redirect("appointments")

def RejectAppointment(request, appointment_id):
    appointment = Appointment.objects.get(pk = appointment_id)
    appointment.approved = "Rejected"
    appointment.save()
    return redirect("appointments")

def SetSchedule(request):
    form = SetScheduleForm(request.POST)
    
    if form.is_valid():
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        schedule = Schedule.objects.create(start_date=start_date, end_date=end_date)

    return render(request, "core/coordinator.html", {"form":form})

def SetMilestones(request):
    form = SetMilestoneForm(request.POST)

    if form.is_valid():
        milestone = form.cleaned_data.get("milestone")
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        milestone = Milestone.objects.create(milestone=milestone, start_date=start_date, end_date=end_date)
    
    return render(request, "core/coordinator.html", {"form2":form})

def UpdateProfile(request):
    return render(request, "core/profile.html")

def StudentProject(request):
    user = request.user
    schedule = user.student.project.schedule
    milestones = Milestone.objects.filter(schedule_id=schedule.id)
    for milestone in milestones:
        remaining_days = milestone.end_date - milestone.start_date
    print (remaining_days)
    return render(request,"core/project/project_progress.html", {"milestones":milestones, "student":user.student,"remaining_days":remaining_days})



