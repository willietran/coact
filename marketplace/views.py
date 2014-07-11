from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from marketplace.forms import *

# Create your views here.
from marketplace.forms import EmailUserCreationForm, LandingForm
from marketplace.models import EmailSignup


def home(request):
    if request.method == "POST":
        form = LandingForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            EmailSignup.objects.create(email=email, name=name)
            return redirect("confirm")
    else:
        form = LandingForm()

    landing = EmailSignup.objects.all()
    data = {"landing_form": form, "landing": landing}
    return render(request, "index.html", data)


def beta(request):
    classroom = Classroom.objects.all()
    class_data = {"classroom": classroom}
    return render(request, "beta.html", class_data)


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })


def create_class(request):
    if request.method == "POST":
        form = CreateClassForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            project = form.cleaned_data['project']
            description = form.cleaned_data['description']
            short_description = form.cleaned_data['short_description']
            teacher = request.user
            screenshot = form.cleaned_data['screenshot']
            cost = form.cleaned_data['cost']
            Classroom.objects.create(title=title, project=project, description=description, teacher=teacher,
                                     screenshot=screenshot, cost=cost, short_description=short_description)
            return redirect("beta")
    else:
        form = CreateClassForm()

    classroom = Classroom.objects.all()
    data = {"classroom_form": form, "classroom": classroom}
    return render(request, "create_class.html", data)


def confirm(request):
    return render(request, "confirm.html")


def class_details(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    classroom_data = {'classroom': classroom}

    return render(request, "class_details.html", classroom_data)


def join_class(request, classroom_id):
    # classroom = Classroom.objects.all()
    # classroom_data = {'classroom': classroom}
    classroom1 = Classroom.objects.get(id=classroom_id)
    classroom_data1 = {'classroom': classroom1}
    # new_student = Learner.objects.get_or_create(name=request.user, hangout=request.user)
    # classroom1.student.add(new_student)
    try:
        new_student = Learner.objects.get(name=request.user)
    except Learner.DoesNotExist:
        new_student = Learner.objects.create(name=request.user, hangout=request.user.email) # Changed to request.user.email. If it doesn't work, change it back to request.user
    classroom1.student.add(new_student)

    return render(request, "join_class.html", classroom_data1)


def edit_class(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if classroom.teacher == request.user:
        if request.method == "POST":
            form = CreateClassForm(request.POST, request.FILES)
            if form.is_valid():
                classroom.title = form.cleaned_data['title']
                classroom.project = form.cleaned_data['project']
                classroom.description = form.cleaned_data['description']
                classroom.short_description = form.cleaned_data['short_description']
                classroom.screenshot = form.cleaned_data['screenshot']
                classroom.cost = form.cleaned_data['cost']
                classroom.save()
                return redirect("beta")
        else:
            form = CreateClassForm(initial={'title': classroom, 'project': classroom, 'description': classroom,
                                            'short_description': classroom, 'screenshot': classroom,
                                            'cost':classroom.cost})
        data = {"form": form, "classroom": classroom}
        return render(request, "registration/edit_class.html", data)
    else:
        return redirect("error")


def error(request):
    return render(request, "error.html")






# def edit_profile(request):
#     if request.method == "POST":
#         form = EditSkillsForm(request.POST)
#         if form.is_valid():
#             skill_1 = form.cleaned_data['skill_1']
#             # skill_2 = form.cleaned_data['skill_2']
#             # skill_3 = form.cleaned_data['skill_3']
#             user = request.user
#             # Get or Create
#             Skill.objects.get_or_create(name=skill_1, user=user)
#             return redirect("beta")
#     else:
#         form = EditSkillsForm
#
#     edit_skills = Skill.objects.all()
#     data = {"edit_skills_form": form, "edit_skills": edit_skills}
#     return render(request, "registration/edit_class.html")





