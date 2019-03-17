import os
import json, io
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.http import FileResponse
from django.utils.text import slugify
from django.contrib import messages

from collections import OrderedDict
from fusioncharts import FusionCharts

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
    form = SelectAvailableDaysForm(request.POST)
    user = request.user
    exists = AvailableDay.objects.filter(supervisor_id = user.supervisor).count()
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

        return render(request, "core/select_available.html",{"form2":form})
    return redirect(SelectAvailableDays)    

def SaveAvailableDays(request):
    form = SelectAvailableDaysForm(request.POST)
    user = request.user
    exists = AvailableDay.objects.filter(supervisor_id = user.supervisor).count()
    supervisor = user.supervisor
    monday_time = form.data["monday"].split(":")
    if monday_time.__len__() >= 2 :
        hour = monday_time[0]
        minute = monday_time[1]
        monday = datetime.time(int(hour),int(minute),00,000000)
        AvailableDay.objects.filter(supervisor_id=supervisor.id).update(monday=monday)
    else:
        pass
    tuesday_time = form.data["tuesday"].split(":")
    if tuesday_time.__len__() >= 2:
        hour = tuesday_time[0]
        minute = tuesday_time[1]
        tuesday = datetime.time(int(hour),int(minute),00,000000)
        AvailableDay.objects.filter(supervisor_id=supervisor.id).update(tuesday=tuesday)
    else:
        pass
    wednesday_time = form.data["wednesday"].split(":")
    if wednesday_time.__len__() >= 2:
        hour = wednesday_time[0]
        minute = wednesday_time[1]
        wednesday = datetime.time(int(hour),int(minute),00,000000)
        AvailableDay.objects.filter(supervisor_id=supervisor.id).update(wednesday=wednesday)
    else:
        pass
    thursday_time = form.data["thursday"].split(":")
    print(thursday_time.__len__())
    if thursday_time.__len__() >= 2:
        hour = thursday_time[0]
        minute = thursday_time[1]
        thursday = datetime.time(int(hour),int(minute),00,000000)
        AvailableDay.objects.filter(supervisor_id=supervisor.id).update(thursday=thursday)
    else:
        pass
    friday_time = form.data["friday"].split(":")
    if friday_time.__len__() >= 2:
        hour = friday_time[0]
        minute = friday_time[1]
        friday = datetime.time(int(hour),int(minute),00,000000)
        AvailableDay.objects.filter(supervisor_id=supervisor.id).update(friday=friday)
    else:
        pass
    saturday_time = form.data["saturday"].split(":")
    if saturday_time.__len__() >= 2:
        hour = saturday_time[0]
        minute = saturday_time[1]
        saturday = datetime.time(int(hour),int(minute),00,000000)
        AvailableDay.objects.filter(supervisor_id=supervisor.id).update(saturday=saturday)
    else:
        pass
    sunday_time = form.data["sunday"].split(":")
    if sunday_time.__len__() >= 2:
        hour = sunday_time[0]
        minute = sunday_time[1]
        sunday = datetime.time(int(hour),int(minute),00,000000)
        AvailableDay.objects.filter(supervisor_id=supervisor.id).update(sunday=sunday)
    else:
        pass
    return redirect(SelectAvailableDays)

def DeleteAvailableDays(request, availableday_id):
    available_day = AvailableDay.objects.get(pk=availableday_id)
    user = request.user
    if user.is_supervisor():
        AvailableDay.filter(pk=availableday_id).update()

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

def ViewProfile(request):
    user = request.user
    if user.is_student:
        student = user.student
        form = UpdateProfileForm(initial={'first_name': student.first_name, 'last_name': student.last_name, 'user_name': user.username,'email': student.email})
    else:
        supervisor = user.supervisor
        form = UpdateProfileForm(initial={'first_name': supervisor.first_name, 'last_name': supervisor.last_name, 'user_name': user.username,'email': supervisor.email})

    return render(request, "core/profile.html", {"form":form})

def project_view(request):
    user = request.user
    if user.is_student:
        return redirect(StudentProject)
    
    elif user.is_supervisor:
        students = Student.objects.filter(supervisor_id = user.supervisor.id)
        return render(request,"core/project/project.html", {"students":students})

def StudentProject(request):
    user = request.user
    form2 = SendCommentForm(request.POST, request.FILES)

    if user.is_student:
        student = user.student
        if student.project:
            schedule = user.student.project.schedule
            milestones = Milestone.objects.filter(schedule_id=schedule.id)
            documents = Document.objects.all()
            comments = Comment.objects.filter(student_id = student.id)

            comment_count = {}
            for milestone in milestones:
                comment_count[milestone.id] = Comment.objects.filter(student_id = student.id, milestone_id=milestone.id).count()
            
            remaining_days = {}
            for milestone in milestones:
                start_date = milestone.start_date
                end_date = milestone.end_date
                now = datetime.datetime.now().date()
                days = end_date - now
                remaining_days[milestone.id] = days.days
            
            
        else:
            form = CreateProjectForm(initial={"abstract_text":" "})
            return render(request, "core/project/project_progress.html",{"form":form})

        return render(request,"core/project/project_progress.html", {"milestones":milestones, "student":student,"remaining_days":remaining_days, "documents":documents, "form2":form2, "comments":comments, "comment_count":comment_count })

def project_supervision_view(request, student_id):
    user = request.user
    form = SendCommentForm(request.POST, request.FILES)
    if user.is_supervisor:
        student = Student.objects.get(pk=student_id)
        schedule = student.project.schedule
        milestones = Milestone.objects.filter(schedule_id=schedule.id)
        documents = Document.objects.filter(student_id = student_id)
        comments = Comment.objects.filter(student_id = student.id)    
        comment_count = {}
        for milestone in milestones:
            comment_count[milestone.id] = Comment.objects.filter(student_id = student.id, milestone_id=milestone.id).count()

        remaining_days = {}
        for milestone in milestones:
            start_date = milestone.start_date
            end_date = milestone.end_date
            now = datetime.datetime.now().date()
            if now > end_date:
                days = 0
                remaining_days[milestone.id] = days
            else:
                days = end_date - now
                remaining_days[milestone.id] = days.days
        return render(request, "core/project/project_supervision.html",  {"milestones":milestones, "student":student,"remaining_days":remaining_days, "documents":documents, "comments":comments, "form":form, "comment_count":comment_count})


def upload_file(request, milestone_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            document = form.cleaned_data["document"]
            title = form.cleaned_data["title"]
            milestone = Milestone.objects.get(pk = milestone_id)            
            if user.is_student:
                student_id = user.student.id
            Document.objects.create(document=document, title=title,student_id = student_id, milestone_id = milestone.id)
    else:
        form = UploadFileForm()
    return redirect(StudentProject)


def download_document(request, document_id):
    item = get_object_or_404(Document, pk=document_id)
    file_name= os.path.join('/media/v3ctor/Projects/FinalYear/newProject/SPMS/media/', str(item.document))
    file_extension = ".docx" # removes dot
    response = FileResponse(item.document, 
        content_type = "file/docx")
    response["Content-Disposition"] = "attachment;"\
        "filename=%s.%s" %(slugify(item.document)[:100], file_extension)
    return response


def createproject_view(request):
    if request.method == "POST":
        form = CreateProjectForm(request.POST, request.FILES)
        user = request.user

        if form.is_valid():
            if user.is_student:
                student = user.student
            else:
                pass
            title = form.cleaned_data.get("title")
            abstract_text = form.cleaned_data.get("abstract")
            document = form.cleaned_data.get("abstract_document")
            schedule = Schedule.objects.get(status=1)
            #Create Abstract
            abstract = Abstract.objects.create(title=title, abstract_text=abstract_text, document=document)
            #Create New Project
            project = Project.objects.create(title=title, schedule_id = schedule.id, abstract_id=abstract.id)
            Student.objects.filter(id = student.id).update(project_id=project.id)
        
        return redirect(StudentProject)
        

def view_comment(request, milestone_id, student_id):
    if request.method == "POST":
        user = request.user
        form = SendCommentForm(request.POST, request.FILES)
        student = Student.objects.get(pk=student_id)
        if form.is_valid():
            text = form.cleaned_data.get("comment")
            if user.is_student:
                Comment.objects.create(text=text, student_id = student.id, supervisor_id=student.supervisor.id, milestone_id=milestone_id, sender = 1)
                return redirect(StudentProject)

            else:
                supervisor_id = student.supervisor_id
                supervisor = Supervisor.objects.get(pk=supervisor_id)
                Comment.objects.create(text=text, student_id = student.id, supervisor_id=student.supervisor.id, milestone_id=milestone_id, sender = 0)
                return redirect(project_supervision_view, student.id)


def UpdateProfile(request):
    user =  request.user
    form = UpdateProfileForm(request.POST, request.FILES)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        user_name = form.cleaned_data.get("user_name")   

    if user.is_authenticated:
        if user.is_student:
            student = user.student
            Student.objects.filter(pk=student.id).update(email=email, first_name=first_name, last_name=last_name)

        else:
            supervisor = user.supervisor
            Supervisor.objects.filter(pk=supervisor.id).update(email=email, first_name=first_name, last_name=last_name)
        
        return redirect(ViewProfile)


def ViewPastProjects(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        user = request.user
        if form.is_valid():
            for phone in form.cleaned_data.get("phone_numbers").splitlines():
                message = form.cleaned_data.get("message")
                access_code = user.profile.access_code
                service_id = user.profile.access_id
                #YourModel.Objects.create(phone_number = phone, message=message)
                #Save Your phone number and message here => each loop saves one phone number and the message 
    pastprojects = PastProject.objects.all()
    students = Student.objects.all()
    return render(request,"core/index.html", {"pastprojects":pastprojects,"students":students})


def CloseProject(request, project_id, student_id):
    PastProject.objects.add(project_id = project_id)
    Project.objects.filter(pk=project_id).update(status=0)
    Student.objects.filter(pk=student_id).update(status=0)
    return response


def CloseMilestone(request, milestone_id, project_id):
    students = Student.objects.all()

    for student in students:
        if student.project_id:
            if student.project_id == project_id:
                student = student
    
    milestone = Milestone.objects.get(pk=milestone_id)
    if milestone.check_status == "NS" or milestone.check_status == "ON":
        pass
    else:
        CompletedMilestones.objects.create(milestone_id=milestone_id, project_id=project_id)
    return redirect(project_supervision_view, student.id)


def CloseProject(request, project_id):
    students = Student.objects.all()
    for student in students:
        if student.project_id:
            if student.project_id == project_id:
                student = student
    
    milestones = Milestone.objects.all()
    completed_milestones = CompletedMilestones.objects.all()
    project_status = False
    for milestone in milestones:
        for completed_milestone in completed_milestones:
            if milestone.id == completed_milestone.milestone_id:
                project_status = True
            else:
                project_status = False
    if project_status == True:
        PastProject.objects.create(project_id=project_id)
        Project.objects.filter(pk=project_id).update(status=False)
    else:
        pass

    return redirect(project_supervision_view, student.id)


def chart_view(request):
    milestones = Milestone.objects.all()
    groups = Group.objects.all()
    group1 = Group.objects.get(pk=1)
    group2 = Group.objects.get(pk=2)
    gantt_info = {
        "chart":{
            "dateformat": "mm/dd/yyyy",
            "caption": "Final Year Project",
            "theme": "ocean",
            "canvasborderalpha": "40",
            "ganttlinealpha": "50"
        },
        
        "tasks":{
            "color": "#5D62B5",
            "task":[

            ]          
        }, 
        "processes" : {
          "headertext": "Task",
          "headeralign": "left",
          "fontsize": "14",
          "isbold": "0",
          "align": "left",
          "process": [
          ] 
        }, 
        "categories":[
            {
              "category":[

              ] 
            },
            {
              "category": [
          {
            "start": "09/10/2018",
            "end": "09/30/2018",
            "label": "September"
          },
          {
            "start": "10/01/2018",
            "end": "10/31/2018",
            "label": "October"
          },
          {
            "start": "11/01/2018",
            "end": "11/30/2018",
            "label": "November"
          },
          {
            "start": "12/01/2018",
            "end": "12/31/2018",
            "label": "December"
          },          
          {
            "start": "01/01/2019",
            "end": "01/31/2019",
            "label": "January"
          },          {
            "start": "02/01/2019",
            "end": "02/28/2019",
            "label": "February"
          },          {
            "start": "03/01/2019",
            "end": "03/31/2019",
            "label": "March"
          },          
          {
            "start": "04/01/2019",
            "end": "04/10/2019",
            "label": "April"
          },
              ]
            }
        ]
    }
    inner_dict = {}
    
    week = 0
    for milestone in milestones:
        gantt_info["tasks"]["task"].append({"start": milestone.start_date.__str__(), "end": milestone.end_date.__str__()})
        gantt_info["processes"]["process"].append({"label" : milestone.milestone_name})
        week += 1
    
    for group in groups:
        if group.group == "S1":
              label = "Semester One"
        else:
              label = "Semester Two"

        gantt_info["categories"][0]["category"].append(
          {"start":group.start_date.__str__(), "end":group.end_date.__str__(), "label":label}
          )
        # gantt_info["categories"][0]["category"].append(
        #   {"start":group2.start_date.__str__(), "end":group2.end_date.__str__(), "label":"Semester Two"})
        # gantt_info["categories"][1]["category"].append({"start": milestone.start_date.__str__(), "end":milestone.end_date.__str_    "label":"W"+ str(week)})       

    # gantt_info["tasks"] = tasks
    # gantt_info["processes"] = processes
    # for milestone in milestones:
    #     processes["process"].append(inner_dict)
    #     tasks["task"].append(inner_dict)
    #     tasks["task"][0]["start"] = milestone.start_date.__str__()
    #     tasks["task"][0]["end"] = milestone.end_date.__str__()
    #     processes["process"][0]["task"] = milestone.milestone_name

    chart = gantt_info  
    gantt_info_json = json.dumps(gantt_info)
    print (gantt_info_json)

    chartObj = FusionCharts(
        'gantt',
        'ex1',
        '1000',
        '500',
        'chart-1',
        'json',
        json.dumps(chart) 
        )

    return render(request, 'fusion/fusion.html', {'output': chartObj.render()})