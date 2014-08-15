from datetime import datetime
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.template.loaders.app_directories import app
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from marketplace.forms import *
import stripe
import requests

# Create your views here.
from marketplace.forms import EmailUserCreationForm, LandingForm
from marketplace.models import EmailSignup


# Initial view just for the home page
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


# Home page for the beta access. Not the landing page to collect e-mail sign ups
def beta(request):
    classroom = Classroom.objects.all()
    class_data = {"classroom": classroom}
    return render(request, "beta-bs.html", class_data)


def class_list(request):
    if request.method == 'GET':
        classroom = Classroom.objects.all()
        class_data = {"classroom": classroom}
        return render(request, "class-list.html", class_data)


# Registration view
def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return redirect("home")
    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })


# View to create a new class
@login_required()
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
    return render(request, "class_create/base.html", data)


# Confirmation page for after people create a new account
def confirm(request):
    return render(request, "confirm.html")


# View to allow people to view details in the class before signing up
def class_details(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    cost_in_cents = classroom.cost*100
    classroom_data = {'classroom': classroom,
                      'cost_in_cents': cost_in_cents}

    return render(request, "class_details-bs.html", classroom_data)


# The button to place a mark on people to measure purchase intent
@login_required()
def join_class(request, classroom_id):
    classroom1 = Classroom.objects.get(id=classroom_id)
    classroom_data1 = {'classroom': classroom1}
    try:
        new_student = Learner.objects.get(name=request.user)
    except Learner.DoesNotExist:
        new_student = Learner.objects.create(name=request.user, hangout=request.user)
    classroom1.student.add(new_student)

    return render(request, "join_class.html", classroom_data1)


# Teacher's ability to edit the class that they created.
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
                return redirect("/details/{}".format(classroom_id))
        else:
            form = CreateClassForm(initial={'title': classroom.title, 'project': classroom.project,
                                            'description': classroom.description,
                                            'short_description': classroom.short_description,
                                            'screenshot': classroom.screenshot,
                                            'cost': classroom.cost})
        data = {"form": form, "classroom": classroom}
        return render(request, "class_create/edit_class.html", data)
    else:
        return redirect("error")


# Allows a teacher to delet their own class.
def delete_class(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    # classroom_data = {'classroom': classroom}
    if classroom.teacher == request.user:
        classroom.delete()
        return redirect("beta")
    else:
        return redirect("error")

    # return render(request, "delete_class.html", classroom_data)


# This is an error page for when people try to game the system
def error(request):
    return render(request, "error.html")


# Users can create a new review on a class. I need to work on this to allow for more information
@login_required()
def create_review(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if classroom.teacher == request.user:
        return redirect('beta')
    else:
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.cleaned_data['review']
                # content = form.cleaned_data['content']
                classroom = Classroom.objects.get(id=classroom_id)
                reviewer = request.user
                Review.objects.create(review=review, classroom=classroom, reviewer=reviewer)
                return redirect('/details/{}'.format(classroom_id))
        else:
            form = ReviewForm(initial={'classroom': classroom.title})
        data = {"form": form, 'classroom': classroom}
        return render(request, "create_review.html", data)


# Viewing people's profiles
@login_required()
def view_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_data = {'user': user}
    return render(request, "view-profile-bs.html", user_data)


def dashboard(request, user_id):
    user = User.objects.get(id=user_id)
    payment_history = Payment.objects.filter(student=user)
    # User Lookup Field "a = Payment.objects.filter(classroom__teacher__username='willietran')"
    teacher_payments = Payment.objects.filter(classroom__teacher__username=user)

    dashboard_data = {'user': user, 'payment_history': payment_history, 'teacher_payments': teacher_payments}

    return render(request, "dashboard.html", dashboard_data)


# Viewing teacher's profiles
def view_teacher(request, user_id):
    teacher = User.objects.get(id=user_id)
    teacher_data = {'teacher': teacher, 'id': user_id}
    return render(request, "view_teacher-bs.html", teacher_data)


@csrf_exempt
def charge(request, classroom_id):

    classroom = Classroom.objects.get(id=classroom_id)
    classroom_data = {'classroom': classroom}

    # Potential: Pull back the classroom teacher for this by doing classroom.teacher and then match it to the
    # username in StripePayments

    stripe_info = StripeKey.objects.get(user=classroom.teacher)
    print "Printing Stripe Connect Key"
    print stripe_info.api_key

    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here https://dashboard.stripe.com/account
    stripe.api_key = stripe_info.api_key

    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']

    # # Create a Customer
    # customer = stripe.Customer.create(
    #     card=token,
    #     description=request.user.email
    # )
    #
    class_cost = classroom.cost*100
    #
    # # Charge the Customer instead of the card
    # stripe.Charge.create(
    #     amount=int(class_cost),  # in cents
    #     currency="usd",
    #     customer=customer.id
    # )
    #
    # Make a new payment transaction object for Payment History
    Payment.objects.create(
        charge_amount=int(classroom.cost),
        classroom=classroom,
        student=request.user,
        date=datetime.now()
    )

    access_token = stripe_info.api_key
    url = "https://api.stripe.com/v1/charges"
    amount = int(class_cost)  # in cents
    currency = "usd"
    card = token

    query_args = {'access_token': access_token,
                  'amount': amount,
                  'currency': currency,
                  'card': card}

    r = requests.post(url, data=query_args)

    print "Printing access token..."
    print access_token
    print r.status_code
    print r.json

    return render(request, 'charge.html', classroom_data)


def landing_page(request):
    return render(request, 'landing.html')


def stripe_connect(request):

    print request

    url = "https://connect.stripe.com/oauth/token"
    client_secret = "sk_test_eBoq5GKhL3wNB1PwDW8owedu"
    code = str(request.GET['code'])
    grant_type = 'authorization_code'

    query_args = {'client_secret': client_secret, 'code': code, 'grant_type': grant_type}
    r = requests.post(url, data=query_args)

    # Accessing the access token that we got from the User OAuth Login
    print r.json['access_token']

    # Creating a stripe Customer Token
    StripeKey.objects.create(
        api_key=r.json['access_token'],
        user=request.user
    )

    return render(request, 'stripe_login.html')


def account(request):
    return render(request, 'account.html')


@csrf_exempt
def calendar(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        jsondata = json.loads(request.body)
        Calendar.objects.get(teacher=user).delete()
        Calendar.objects.create(teacher=user)
        calendar = Calendar.objects.get(teacher=user)
        for item in jsondata:
            splitted = item.split("-")
            print splitted
            Slot.objects.create(calendar=calendar,day=splitted[0],time=splitted[1])

    user = User.objects.get(id=user_id)
    Calendar.objects.get_or_create(teacher=user)
    calendar = Calendar.objects.get(teacher=user)
    slots = Slot.objects.filter(calendar=calendar)

    slots_list=[]
    for item in slots:
        # print item.day
        slots_list.append(item.day+'-'+str(item.time))

    slots_list_json  =json.dumps(slots_list)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = []

    for i in range(1,24):
            hours.append(i)

    data = {'days':days, 'hours':hours, 'slots':slots_list, 'slots_list_json': slots_list_json, 'teacherid':user_id}

    return render(request, 'calendar.html', data)


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





