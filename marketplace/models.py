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


# I don't understand the relationships you've built here. You would still have to do: learner.hangout.hangout
# to get to the `hangout` attribute on the User model. Naming these fields as `name` and `hangout` doesn't change that
class Learner(models.Model):
    # See python documentation on modeling here: https://docs.djangoproject.com/en/dev/topics/db/models/
    name = models.ForeignKey(User, related_name='student_name')
    hangout = models.ForeignKey(User, related_name='student_hangout')

    def __unicode__(self):
        return u"{}".format(self.name)


# Are you actually using this model?
# If yes, it would make more sense for Learner and Teacher to either 1) be the same model with a field that has options
# for either learner or teacher or 2) if they must be different models, have them inherit from the same base abstract
# model so you don't have to repeat this code
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
    # cost = models.FloatField()
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    teacher = models.ForeignKey(User, related_name='classroom_teacher')
    student = models.ManyToManyField(Learner, related_name='classroom_learner')
    screenshot = models.ImageField(upload_to='class_img', null=True)

    def __unicode__(self):
        return u"{}".format(self.title)


class Review(models.Model):
    review = models.CharField(max_length=140)
    # content = models.CharField(max_length=400)
    classroom = models.ForeignKey(Classroom, related_name='classroom_review')
    reviewer = models.ForeignKey(User, related_name='reviewer_review')

    def __unicode__(self):
        return u"{}".format(self.review)




# class Skill(models.Model):
#     # Look into Django ModelFormSet
#     name = models.CharField(max_length=20)
#     # name_2 = models.CharField(max_length=20)
#     # name_3 = models.CharField(max_length=20)
#     user = models.ForeignKey(User, related_name='user_skill')
#
#     def __unicode__(self):
#         return u"{}".format(self.name)
