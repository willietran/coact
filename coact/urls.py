from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^beta/$', 'marketplace.views.beta', name='beta'),
    url(r'^$', 'marketplace.views.beta', name='home'),
    url(r'^landing_page/$', 'marketplace.views.landing_page', name='landing_page'),

    # User Registration
    url(r'^register/$', 'marketplace.views.register', name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^confirm/$', 'marketplace.views.confirm', name='confirm'),
    (r'^accounts/', include('registration.backends.default.urls')),

    # url(r'^edit_profile/$', 'marketplace.views.edit_profile', name='edit_profile'),

    # Password Reset
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    # Support old style base36 password reset links; remove in Django 1.7
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    'django.contrib.auth.views.password_reset_confirm_uidb36'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    'django.contrib.auth.views.password_reset_confirm',
    name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    # Classroom Creation
    url(r'^create_class/$', 'marketplace.views.create_class', name='create_class'),
    url(r'^class_list/$', 'marketplace.views.class_list', name='class_list'),
    url(r'^details/(?P<classroom_id>[0-9]+)/$', 'marketplace.views.class_details', name='class_details'),
    url(r'^details/(?P<classroom_id>[0-9]+)/join/$', 'marketplace.views.join_class', name='join_class'),
    url(r'^details/(?P<classroom_id>[0-9]+)/edit/$', 'marketplace.views.edit_class', name='edit_class'),
    url(r'^details/(?P<classroom_id>[0-9]+)/delete/$', 'marketplace.views.delete_class', name='delete_class'),
    # url(r'^details/(?P<classroom_id>[0-9]+)/charge/$', 'marketplace.views.charge', name='charge'),
    url(r'^error/$', 'marketplace.views.error', name='error'),

    # Classroom Review
    url(r'^details/(?P<classroom_id>[0-9]+)/create_review/$', 'marketplace.views.create_review', name='create_review'),

    # Calendar
    url(r'^calendar/', include('calendarium.urls')),

    # View Profile
    url(r'^view/(?P<user_id>[0-9]+)/$', 'marketplace.views.view_profile', name='view_profile'),
    url(r'^view_teacher/(?P<user_id>[0-9]+)/$', 'marketplace.views.view_teacher', name='view_teacher'),

    # Django-Messages
    url(r'^messages/', include('django_messages.urls')),

    # Payment Charging
    url(r'^charge/(?P<user_id>[0-9]+)/$', 'marketplace.views.charge', name='charge'),
    url(r'^stripe_connect/$', 'marketplace.views.stripe_connect', name='stripe_connect'),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

