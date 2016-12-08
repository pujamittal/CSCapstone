"""ProjectsApp URL Configuration

Created by Harris Christiansen on 10/02/16.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/all$', views.getProjects, name='Projects'),
    url(r'^project$', views.getProject, name='Project'),
    url(r'^create_project$', views.getCreateProject, name='Create Project'),
    url(r'^bookmark/add$', views.getBookmarkSuccess, name='Bookmark Success'),
    url(r'^project/edit$', views.getEditProject, name='Edit Project'),
    url(r'^bookmark/remove$', views.unBookmark, name='Remove Bookmark'),
    url(r'^project/delete$', views.deleteProject, name='Delete Project'),
]