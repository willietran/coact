from django.contrib.auth.models import AbstractUser
from django.db import models
# from simple_email_confirmation import SimpleEmailConfirmationUserMixin


# Create your models here.


class EmailSignup(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return u"{}".format(self.email)


class User(AbstractUser):
    hangout = models.CharField(max_length=30)
    image = models.ImageField(upload_to='user_img', null=True)
    about = models.TextField(null=True)
    occupation = models.CharField(max_length=30, null=True)


class Learner(models.Model):
    # See python documentation on modeling here: https://docs.djangoproject.com/en/dev/topics/db/models/
    name = models.ForeignKey(User, related_name='student_name')
    hangout = models.ForeignKey(User, related_name='student_hangout')

    def __unicode__(self):
        return u"{}".format(self.name)


class Teacher(models.Model):
    name = models.ForeignKey(User, related_name='teacher_name')
    hangout = models.ForeignKey(User, related_name='teacher_hangout')

    def __unicode__(self):
        return u"{}".format(self.name)


class Classroom(models.Model):
    title = models.CharField(max_length=140)
    project = models.CharField(max_length=50)
    short_description = models.CharField(max_length=160)
    description = models.TextField()
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    teacher = models.ForeignKey(User, related_name='classroom_teacher')
    student = models.ManyToManyField(Learner, related_name='classroom_learner')
    screenshot = models.ImageField(upload_to='class_img', null=True)
    api_key = models.CharField(max_length=100, null=True, default='0000')

    def __unicode__(self):
        return u"{}".format(self.title)


class Calendar(models.Model):
    teacher = models.ForeignKey(User, related_name='calendar_teacher')
    slot = models.ManyToManyField('Slot', related_name='calendar_slot')


class Slot(models.Model):
    calendar = models.ForeignKey(Calendar, related_name='slot_calendar')
    day = models.CharField(max_length=10)
    time = models.IntegerField()


class Review(models.Model):
    review = models.CharField(max_length=140)
    classroom = models.ForeignKey(Classroom, related_name='classroom_review')
    reviewer = models.ForeignKey(User, related_name='reviewer_review')

    def __unicode__(self):
        return u"{}".format(self.review)


class Payment(models.Model):
    charge_amount = models.DecimalField(decimal_places=2, max_digits=10)
    classroom = models.ForeignKey(Classroom, related_name='payment_classroom')
    student = models.ForeignKey(User, related_name='payment_student')
    date = models.DateTimeField()

    def __unicode__(self):
        return u"{}'s payment to {}".format(self.student, self.classroom)


class StripeKey(models.Model):
    api_key = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='stripe_key_user')

    def __unicode__(self):
        return u"{}'s Access Token".format(self.user)