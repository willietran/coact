from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class EmailSignup(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return u"{}".format(self.email)


class User(AbstractUser):
    hangout = models.CharField(max_length=30)
    image = models.ImageField(null=True, upload_to='user_img')


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
    short_description = models.CharField(max_length=140)
    description = models.TextField()
    cost = models.FloatField()
    teacher = models.ForeignKey(User, related_name='classroom_teacher')
    student = models.ManyToManyField(Learner, related_name='classroom_learner')
    screenshot = models.ImageField(upload_to='class_img', null=True)

    def __unicode__(self):
        return u"{}".format(self.title)







# class Skill(models.Model):
#     # Look into Django ModelFormSet
#     name = models.CharField(max_length=20)
#     # name_2 = models.CharField(max_length=20)
#     # name_3 = models.CharField(max_length=20)
#     user = models.ForeignKey(User, related_name='user_skill')
#
#     def __unicode__(self):
#         return u"{}".format(self.name)