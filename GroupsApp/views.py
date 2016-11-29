"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from . import models
from . import forms

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.select_related().all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        context = {
            'group' : in_group,
            'userIsMember': is_member,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        projects_list = models.Project.objects.all()
        return render(request, 'groupform.html',{
        'projects': projects_list,
    })
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                try:
                    project = models.Project.objects.get(project_id=form.cleaned_data['project'])
                except ObjectDoesNotExist:
                    return render(request, 'groupform.html', {'error': 'Error: That project does not exist!'})
                new_group.project = project
                new_group.save()
                new_group.members.add(request.user)
                new_group.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        request.user.group_set.add(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')


def getGroupAddMemberForm(request):
    if request.user.is_authenticated():
        context = {
            'name': request.GET.get('name', ''),
        }
        return render(request, 'groupaddmemberform.html',context)
    # render error page if user is not logged in

    return render(request, 'autherror.html')

def getGroupAddMemberFormSuccess(request):
    # return None
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupAddMemberForm(request.POST)
            if form.is_valid():
                group_to_join = models.Group.objects.get(name__exact=form.cleaned_data['name'])
                try:
                    user = models.MyUser.objects.get(email__exact=form.cleaned_data['email'])
                except ObjectDoesNotExist:
                    return render(request, 'groupaddmemberform.html', {'error': 'Error: That user does not exist!'})

                group_to_join.members.add(user)
                group_to_join.save()
                user.group_set.add(group_to_join)
                user.save()
                context = {
                    'name' : form.cleaned_data['name'],
                    'email' : form.cleaned_data['email'],
                }
                return render(request, 'groupaddmemberformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupaddmemberform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')