from datetime import datetime
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from marketplace.forms import *
import stripe
import requests

# Create your views here.
from marketplace.forms import EmailUserCreationForm, LandingForm
from marketplace.models import EmailSignup

# All of your regular django Forms should implement a save function, that way the saving logic is left out of the views
# and all stored in forms.py for better organization and reuse of the forms

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
    return render(request, "old_html_files/index.html", data)


# Home page for the beta access. Not the landing page to collect e-mail sign ups
def beta(request):
    classroom = Classroom.objects.all()
    class_data = {"classroom": classroom}
    return render(request, "beta-bs.html", class_data)


def class_list(request):
    if request.method == 'GET':
        classroom = Classroom.objects.all()
        class_data = {"classroom": classroom}
        # Should try to keep a common syntax either '-' or '_' (preferably) for template folders and files
        return render(request, "old_html_files/class-list.html", class_data)


# Registration view
def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            text_content = 'Thanks for signing up to Coact! Feel free to browse or start earning money by teaching ' \
                           'a class!'
            html_content = '<h2>{}! Thank you!</h2> <div><p>Feel free to browse or start earning money by teaching ' \
                           'a class at www.coact.io</p></div>'.format(user.first_name)
            msg = EmailMultiAlternatives("Welcome!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
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
            # Create the Classroom
            title = form.cleaned_data['title']
            project = form.cleaned_data['project']
            description = form.cleaned_data['description']
            short_description = form.cleaned_data['short_description']
            teacher = request.user
            screenshot = form.cleaned_data['screenshot']
            cost = form.cleaned_data['cost']
            Classroom.objects.create(title=title, project=project, description=description, teacher=teacher,
                                     screenshot=screenshot, cost=cost, short_description=short_description)
            # Send the User an e-mail
            text_content = 'Congratulations! Your class is now available for anyone to register!'
            html_content = '<h2>Success! Classroom created!</h2> <div><p>{} is now available for any student to take.' \
                           ' Start getting students to your site so you can earn money!</p></div>'.format(title)
            msg = EmailMultiAlternatives("Classroom created!", text_content, settings.DEFAULT_FROM_EMAIL,
                                         [request.user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect("beta")
        else:
            return redirect("beta")
    else:
        form = CreateClassForm()

    print request

    url = "https://connect.stripe.com/oauth/token"
    client_secret = "sk_test_eBoq5GKhL3wNB1PwDW8owedu"
    code = str(request.GET['code'])
    grant_type = 'authorization_code'

    query_args = {'client_secret': client_secret, 'code': code, 'grant_type': grant_type}
    r = requests.post(url, data=query_args)

    # Accessing the access token that we got from the User OAuth Login
    print r.text
    print r.json
    print r.json['access_token']
    
    # There should be some Stripe error checking here incase something goes wrong

    # Creating a stripe Customer Token
    StripeKey.objects.create(
        api_key=r.json['access_token'],
        user=request.user
    )

    # Creating a Recipient
    stripe.Recipient.create(
        name=request.user.first_name,
        description=request.user.email,
        type='individual',
        api_key=r.json['access_token']
    )

    # Creating user as a customer as well
    stripe.Customer.create(
        description=request.user.email,
        api_key=r.json['access_token']
    )

    classroom = Classroom.objects.all()
    data = {"classroom_form": form, "classroom": classroom}
    return render(request, "class_create/base.html", data)


# Confirmation page for after people create a new account
def confirm(request):
    return render(request, "old_html_files/confirm.html")


# View to allow people to view details in the class before signing up
def class_details(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    cost_in_cents = classroom.cost*100
    classroom_data = {'classroom': classroom,
                      'cost_in_cents': cost_in_cents}

    # Could use Learner.objects.get_or_create() here
    # Tracks which students have visited a page
    try:
        new_student = Learner.objects.get(name=request.user)
    except Learner.DoesNotExist:
        new_student = Learner.objects.create(name=request.user, hangout=request.user)
    classroom.student.add(new_student)

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

    return render(request, "old_html_files/join_class.html", classroom_data1)


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


# Allows a teacher to delete their own class.
def delete_class(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
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
        return render(request, "old_html_files/create_review.html", data)


# Viewing people's profiles
@login_required()
def view_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_data = {'user': user}
    return render(request, "view-profile-bs.html", user_data)


def dashboard(request, user_id):
    user = User.objects.get(id=user_id)
    if user.id != request.user.id:
        return redirect("beta")
    else:
        # can just do Classroom.objects.filter(teacher=request.user)
        classroom = Classroom.objects.filter(teacher__id=request.user.id)
        payment_history = Payment.objects.filter(student=request.user).order_by('-date')
        teacher_payments = Payment.objects.filter(classroom__teacher__username=request.user).order_by('-date')
        teacher_may = teacher_payments.filter(date__month='5')
        teacher_june = teacher_payments.filter(date__month='6')
        teacher_july = teacher_payments.filter(date__month='7')
        teacher_august = teacher_payments.filter(date__month='8')

        dashboard_data = {'user': user, 'payment_history': payment_history, 'teacher_payments': teacher_payments,
                          'may': teacher_may, 'june': teacher_june, 'july': teacher_july, 'august': teacher_august,
                          'classroom': classroom}

        return render(request, "dashboard.html", dashboard_data)


# Viewing teacher's profiles
def view_teacher(request, user_id):
    # Will error if a non-existing teacher's id is used
    teacher = User.objects.get(id=user_id)
    teacher_data = {'teacher': teacher, 'id': user_id}
    return render(request, "view_teacher-bs.html", teacher_data)


@csrf_exempt
def charge(request, classroom_id):

    classroom = Classroom.objects.get(id=classroom_id)
    classroom_data = {'classroom': classroom}

    stripe_info = StripeKey.objects.filter(user=classroom.teacher).latest('id')

    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here https://dashboard.stripe.com/account
    stripe.api_key = 'sk_test_eBoq5GKhL3wNB1PwDW8owedu'

    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']

    # Converting classroom cost to cents
    class_cost = classroom.cost*100

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

    query_args = {'amount': amount,
                  'currency': currency,
                  'card': card}

    r = requests.post(url, data=query_args, headers={'Authorization': 'Bearer {}'.format(access_token)})

    print "Printing access token..."
    print access_token
    print r.status_code
    print r.json

    # Send the recipient an e-mail
    text_content = 'A new student has purchased one of your classes!'
    html_content = '<h2>New student!</h2> <div><p>A new student has enrolled in {}. Send them a message to welcome ' \
                   'them to the class and let them know how to prepare. Come check it out at www.coact.io.</p>' \
                   '</div>'.format(classroom.title)
    msg = EmailMultiAlternatives("A new student has enrolled in one of your classes!", text_content,
                                 settings.DEFAULT_FROM_EMAIL, [classroom.teacher.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # Send the student an e-mail
    text_content = 'You have enrolled in {}!'.format(classroom.title)
    html_content = '<h2>Thank you for enrolling in {}!</h2> <div><p>You should be receiving a message from {} shortly,' \
                   ' but if you are so eager, feel free to send them an e-mail here, {}.</p>' \
                   '</div>'.format(classroom.title, classroom.teacher.first_name, classroom.teacher.email)
    msg = EmailMultiAlternatives("You have enrolled in a new class!", text_content, settings.DEFAULT_FROM_EMAIL,
                                 [classroom.teacher.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return render(request, 'charge.html', classroom_data)


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


def stripe_setup(request):
    return render(request, 'class_create/stripe_setup.html')





