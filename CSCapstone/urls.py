#CSCapstone Master URL Configuration

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^', include('AuthenticationApp.urls')),
	url(r'^', include('CSCapstoneApp.urls')),
	url(r'^', include('ProjectsApp.urls')),
    url(r'^', include('CompaniesApp.urls')),
    url(r'^', include('GroupsApp.urls')),
	url(r'^', include('UniversitiesApp.urls'))
]
