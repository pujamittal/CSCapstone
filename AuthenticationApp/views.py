"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterForm, UpdateForm
from .models import MyUser, Student, Teacher, Engineer

def auth_login(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if next_url is None:
        next_url = "/"
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
            login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            messages.warning(request, 'Invalid username or password.')
            
    context = {
        "form": form,
        "page_name" : "Login",
        "button_value" : "Login",
        "links" : ["register"],
    }
    return render(request, 'auth_form.html', context)

def auth_logout(request):
    logout(request)
    messages.success(request, 'Success, you are now logged out')
    return render(request, 'index.html')

def auth_register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    form = RegisterForm(request.POST or None)
    
    if form.is_valid():
        usertype = form.cleaned_data['usertype']

        if usertype == 'Student':
            new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
                password=form.cleaned_data['password2'], 
                first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'])
            new_user.is_student = True
            new_user.save()         
            new_student = Student(user=new_user, university=form.cleaned_data['university'])
            new_student.save()
            login(request, new_user);   
            messages.success(request, 'Success! Your student account was created.')
            return render(request, 'index.html')
        elif usertype == 'Teacher':
            new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
                password=form.cleaned_data['password2'], 
                first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'])
            new_user.is_teacher = True
            new_user.save()
            new_teacher = Teacher(user=new_user, university=form.cleaned_data['university'])
            new_teacher.save()
            login(request, new_user);
            messages.success(request, 'Success! Your teacher account was created.')
            return render(request, 'index.html')
        elif usertype == 'Engineer':
            new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
                password=form.cleaned_data['password2'], 
                first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'])
            new_user.is_engineer = True
            new_user.save()
            new_engineer = Engineer(user=new_user)
            new_engineer.about = form.cleaned_data['about']
            new_engineer.almamater = form.cleaned_data['almamater']
            new_engineer.company = form.cleaned_data['company']
            new_engineer.save()
            login(request, new_user);
            messages.success(request, 'Success! Your engineer account was created.')
            return render(request, 'index.html')

    context = {
        "form": form,
        "page_name" : "Register",
        "button_value" : "Register",
        "links" : ["login"],
    }
    return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
    if request.user.is_authenticated():
        user_id = int(request.GET.get('id'))
        user = MyUser.objects.filter(id=user_id)[0]
        
        if int(request.user.id) == user_id or request.user.is_admin == True:
            form = UpdateForm(request.POST or None, instance=user)

            if form.is_valid():
                form.save()
                messages.success(request, 'Success, your profile was saved!')

            context = {
                "form": form,
                "page_name" : "Update",
                "button_value" : "Update",
                "links" : ["logout"],
            }
            return render(request, 'auth_form.html', context)
        else:
            context = {
                "message": "You do not have permission to update this profile" 
            }
            return render(request, 'baseerror.html', context)

    return render(request, 'autherror.html')

def view_profile(request):
    if request.user.is_authenticated():
        user_id = int(request.GET.get('id'))
        user = MyUser.objects.filter(id=user_id)[0]
        usertype = "Admin"

        if user.is_student == True:
            usertype = "Student"
        elif user.is_teacher == True:
            usertype = "Teacher"
        elif user.is_engineer == True:
            usertype = "Engineer"

        if user.is_admin == True and request.user.is_admin == True:
            context = {
                "user": user, 
                "bookmarks": user.bookmarks,
                "usertype": usertype
            }
            return render(request, 'profile.html', context)
        elif user.is_admin == False:
            context = {
                "user": user, 
                "bookmarks": user.bookmarks,
                "usertype": usertype
            }
            return render(request, 'profile.html', context)
        else:
            context = {
                "message": "You cannot access this profile."
            }
            return render(request, 'baseerror.html', context)

    return render(request, 'autherror.html')

def getStudents(request):
    if request.user.is_authenticated():
        if (request.user.is_admin == True):
            user_list = []
            try:
                user_list = Student.objects.all()
            except Exception as ex:
                pass
            return render(request, 'students.html', {
                'users': user_list
            })
        else:
            context = {
                "message": "You do not have permission to do this."
            }

            return render(request, "baseerror.html", context)

    return render(request, 'autherror.html')

def getTeachers(request):
    if request.user.is_authenticated():
        if (request.user.is_admin == True):
            user_list = []
            try:
                user_list = Teacher.objects.all()
            except Exception as ex:
                pass
            return render(request, 'teachers.html', {
                'users': user_list
            })
        else:
            context = {
                "message": "You do not have permission to do this."
            }

            return render(request, "baseerror.html", context)

    return render(request, 'autherror.html')

def getEngineers(request):
    if request.user.is_authenticated():
        if (request.user.is_admin == True):
            user_list = []
            try:
                user_list = Engineer.objects.all()
            except Exception as ex:
                pass
            return render(request, 'engineers.html', {
                'users': user_list
            })
        else:
            context = {
                "message": "You do not have permission to do this."
            }

            return render(request, "baseerror.html", context)

    return render(request, 'autherror.html')