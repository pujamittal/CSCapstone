"""GroupsApp URL

Created by Naman Patwari on 10/10/2016.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^group/all$', views.getGroups, name='Groups'),
    url(r'^groupcommentdelete$', views.groupCommentDelete, name='groupCommentDelete'),
    url(r'^group/comment$', views.commentGroup, name='commentGroup'),
	url(r'^group/form$', views.getGroupForm, name='GroupForm'),
    url(r'^group/formsuccess$', views.getGroupFormSuccess, name='GroupFormSuccess'),
    url(r'^group/join$', views.joinGroup, name='GJoin'),
    url(r'^group/unjoin$', views.unjoinGroup, name='GUnjoin'),
    url(r'^group$', views.getGroup, name='Group'),
    url(r'^group/addmember$', views.getGroupAddMemberForm, name='GroupAddMemberForm'),
    url(r'^group/addmembersuccess$', views.getGroupAddMemberFormSuccess, name='GroupAddMemberFormSuccess'),
    url(r'^group/assignproject$', views.getGroupAssignProjectForm, name='GroupAssignProjectForm'),
    url(r'^group/dropproject$', views.dropProject, name='GroupDropProject')
]