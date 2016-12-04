"""AuthenticationApp URL Configuration

Created by Naman Patwari on 10/4/2016.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.auth_login, name='Login'),
    url(r'^logout$', views.auth_logout, name='Logout'),
    url(r'^register$', views.auth_register, name='Register'),
    url(r'^update$', views.update_profile, name='UpdateProfile'),    
    url(r'^profile$', views.view_profile, name='ViewProfile'),
    url(r'^student/all$', views.getStudents, name='GetStudents'),
    url(r'^teacher/all$', views.getTeachers, name='GetTeachers'),
    url(r'^engineer/all$', views.getEngineers, name='GetEngineers'),
]