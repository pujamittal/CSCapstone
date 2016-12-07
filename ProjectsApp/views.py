"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render

from .forms import CreateProjectForm, ProjectEditForm
from .models import Project

def getProjects(request):
    projects_list = []
    try:
        projects_list = Project.objects.all()
    except Exception as ex:
        pass
    return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
    project_id = int(request.GET.get('id'))
    project = Project.objects.filter(project_id=project_id)[0]
    owner = project.created_by
    print(owner)
    is_owner = False

    print(owner.id)
    print(request.user.id)

    if owner.id == request.user.id:
        is_owner = True

    context = {
        "project": project,
        "project_id": project_id,
        "is_owner": is_owner
    }
    return render(request, 'project.html', context)

def getCreateProject(request):
    if request.user.is_authenticated():
        if request.user.is_engineer == True or request.user.is_admin == True:
            if request.method == 'POST':
                form = CreateProjectForm(request.POST)
                if form.is_valid():
                    new_project = Project(
                        name=form.cleaned_data['name'], 
                        description=form.cleaned_data['description'],
                        company=form.cleaned_data['company'],
                        language=form.cleaned_data['language'],
                        experience=form.cleaned_data['experience'],
                        speciality=form.cleaned_data['speciality'],
                        created_by=request.user
                    )
                    new_project.save()

                    request.user.engineer.projects.add(new_project)
                    request.user.engineer.save()
                    
                    context = {
                        'name' : form.cleaned_data['name'],
                        'project_id' : new_project.project_id
                    }
                    return render(request, 'projectformsuccess.html', context)
                else:
                    return render(request, 'create_project.html', { 'error' : 'Error: Project failed to create.' })
            else:
                form = CreateProjectForm()
                context = {
                    "form": form,
                    "button_value": "Create Project",
                    "status": 'created'
                }
                return render(request, 'create_project.html', context)
        else:
            return render(request, 'baseerror.html', { "message": "Only engineers can create projects." })

def getEditProject(request):
    if request.user.is_authenticated():
        if request.user.is_engineer == True or request.user.is_admin == True:
            if request.method == 'POST':
                project_id = request.GET.get('id', 'None')
                project = Project.objects.get(pk=project_id)

                if project.created_by.id == request.user.id:
                    form = ProjectEditForm(request.POST)
                    if form.is_valid():
                        project.name = form.cleaned_data['name']
                        project.description = form.cleaned_data['description']
                        project.company = form.cleaned_data['company']
                        project.language = form.cleaned_data['language']
                        project.experience=form.cleaned_data['experience'],
                        project.speciality=form.cleaned_data['speciality']
                        project.save()

                        context = {
                            'name': form.cleaned_data['name'],
                            'project_id': project.project_id,
                            'status': 'updated'
                        }
                        return render(request, 'projectformsuccess.html', context)
                    else:
                        return render(request, 'update_project.html', { 'error' : 'Error: Project failed to update.' })
                else:
                    return render(request, 'baseerror.html', { "message": "Only engineers can edit projects." })
            else:
                form = CreateProjectForm()
                context = {
                    "form": form,
                    "button_value": "Update Project"
                }
                return render(request, 'update_project.html', context)
        else:
            return render(request, 'baseerror.html', { "message": "Only engineers can edit projects." })

def getBookmarkSuccess(request):
    if request.user.is_authenticated():
        project_id_to_bookmark = request.GET.get('project_id', 'None')
        proj = Project.objects.get(pk=project_id_to_bookmark)
        request.user.bookmarks.add(proj)

        context = { 
            "name": proj.name,
            "project_id": project_id_to_bookmark,
            "isBookmarked": True
        }

        return render(request, 'bookmark_success.html', context)
    return render(request, 'autherror.html')

def unBookmark(request):
    if request.user.is_authenticated():
        project_id_to_bookmark = request.GET.get('project_id', 'None')
        proj = Project.objects.get(pk=project_id_to_bookmark)
        request.user.bookmarks.remove(proj)
        request.user.save()
        # context = { 
        #     "name": proj.name,
        #     "project_id": project_id_to_bookmark,
        #     "isBookmarked": False
        # }

        return render(request, 'remove_bookmark_success.html')
    return render(request, 'autherror.html')
