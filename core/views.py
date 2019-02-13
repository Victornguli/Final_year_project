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
    if form.is_valid():
        user = request.user
        date = form.cleaned_data.get("date")
        time = form.cleaned_data.get("time")
        appointment = Appointment.objects.create(date=date, time=time, student_id= user.student.id)
        print ("Appointment Saved")
        return render(request, 'core/request-appointment.html',{"form":form})

    
    return render(request,'core/request-appointment.html',{"form":form})
        # return render(request, "core/request-appointment.html")


def SelectAvailableDays(request):
    form =  SelectAvailableDaysForm(request.POST)
    if form.is_valid():
        days = form.cleaned_data.get("day")
        time = form.cleaned_data.get("time")

        available_day = AvailableDay.objects.create(day=days, time=time)

        return render(request, "core/request-appointment.html" , {"form2":form})
    return render(request, "core/request-appointment.html" , {"form2":form})    


def ViewAvailableDays(request):
    days = AvailableDay.objects.all()
    appointments = Appointment.objects.all()
    students = Student.objects.all()
    return render(request, "core/request-appointment.html" , {"days":days, "appointments":appointments, "students":students })    