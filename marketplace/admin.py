from django.contrib import admin
from marketplace.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(EmailSignup)
admin.site.register(Learner)
admin.site.register(Classroom)
admin.site.register(Review)
admin.site.register(Calendar)
admin.site.register(Slot)