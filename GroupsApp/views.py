"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

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

def commentGroup(request):
    group_id = int(request.GET.get('id'))
    group = models.Group.objects.filter(id=group_id)[0]
    # form = CreateProjectForm(request.POST)
    comment = models.GroupComment(group=group,comment=request.POST.get('comment', 'None'),user=request.user)
    comment.save()

    return HttpResponseRedirect('/group?name=%s' % group.name)



def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        skill = str(in_group.get_best_member_skill())

        try:
            projects = models.Project.objects.filter(language=skill)
        except models.Project.DoesNotExist:
            projects = None

        comments = models.GroupComment.objects.filter(group_id=in_group.id)


        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'best_skill': skill,
            'projects': projects,
            'comments': comments,
            'me': request.user.id,
            'form': forms.CkEditorForm(request.POST or None)
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_admin == True:
            projects_list = models.Project.objects.all()
            return render(request, 'groupform.html',{ 'projects': projects_list })
        else:
            return render(request, 'baseerror.html', { "message": "You do not have permission to create a group." })
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_admin == True:
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
        else:
            return render(request, 'baseerror.html', { "message": "You do not have permission to create a group." })
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_admin == True:
            in_name = request.GET.get('name', 'None')
            in_group = models.Group.objects.get(name__exact=in_name)
            in_group.members.add(request.user)
            in_group.save()
            request.user.student.groups.add(in_group)
            request.user.student.save()
            context = {
                'group' : in_group,
                'userIsMember': True,
            }
            return render(request, 'group.html', context)
        else:
            return render(request, 'baseerror.html', { "message": "Only students can join groups." })
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_admin == True:
            in_name = request.GET.get('name', 'None')
            in_group = models.Group.objects.get(name__exact=in_name)
            in_group.members.remove(request.user)
            in_group.save();
            request.user.student.groups.remove(in_group)
            request.user.student.save()
            context = {
                'group' : in_group,
                'userIsMember': False,
            }
            return render(request, 'group.html', context)
        else:
            return render(request, 'baseerror.html', { "message": "Only students can join groups." })
    return render(request, 'autherror.html')

def getGroupAddMemberForm(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_admin == True:
            group_name = request.GET.get('name', 'None')
            group = models.Group.objects.get(name__exact=group_name)
            is_member = group.members.filter(email__exact=request.user.email)

            if not is_member:
                return render(request, 'baseerror.html', {"message": "Only members of this group can add members." })
            else:
                context = {
                    'name': request.GET.get('name', ''),
                }
                return render(request, 'groupaddmemberform.html',context)
        else:
            return render(request, 'baseerror.html', { "message": "You do not have permission to add members." })   
    return render(request, 'autherror.html')

def getGroupAddMemberFormSuccess(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_admin == True:
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
                    user.student.groups_set.add(group_to_join)
                    user.save()
                    context = {
                        'name' : form.cleaned_data['name'],
                        'email' : form.cleaned_data['email'],
                    }
                    return render(request, 'groupaddmemberformsuccess.html', context)
            else:
                form = forms.GroupForm()
            return render(request, 'groupaddmemberform.html')
        else:
            return render(request, 'baseerror.html', { "message": "You do not have permission to add members." })
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupAssignProjectForm(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_admin == True:
            group_pk = request.GET.get('group_pk', 'None')
            group = models.Group.objects.get(pk__exact=group_pk)
            is_member = group.members.filter(email__exact=request.user.email)

            if not is_member:
                return render(request, 'baseerror.html', {"message": "Only members of this group can assign projects." })
            else:
                form = forms.GroupAssignProjectForm(request.POST or None)

                if form.is_valid():
                    group.project = form.cleaned_data['project']
                    group.save()

                    context = {
                        'group' : group,
                        'userIsMember': is_member,
                    }
                    return render(request, 'group.html', context)

                context = {
                    "form": form
                }
                return render(request, 'groupassignprojectform.html', context)
        else:
            return render(request, 'baseerror.html', { "message": "You do not have permission to assign projects." })   
    return render(request, 'autherror.html')

def dropProject(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_admin == True:
            group_id = request.GET.get('id', 'None')
            group = models.Group.objects.get(id__exact=group_id)
            is_member = group.members.filter(email__exact=request.user.email)

            if is_member:
                group.project = None
                group.save()

                context = {
                    'group' : group,
                    'userIsMember': is_member,
                }
                return render(request, 'group.html', context)
            else:
                return render(request, 'baseerror.html', { "message": "Only members of this group can drop projects." })
        else:
            return render(request, 'baseerror.html', { "message": "You do not have permission to drop projects." })   
    return render(request, 'autherror.html')


def groupCommentDelete(request):
    group_name = request.GET.get('rdr', 'None')
    comment_id = request.GET.get('id', 'None')

    comm = models.GroupComment.objects.get(comment_id=comment_id)
    comm.delete()
    return HttpResponseRedirect('/group?name=%s' % group_name)

