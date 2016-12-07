"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from AuthenticationApp.models import MyUser, Student, Teacher, Engineer

def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember': is_member,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'], 
                                             photo=request.FILES['photo'],  
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinUniversity(request):
    if request.user.is_authenticated():
        if (request.user.is_student == True or request.user.is_teacher == True or request.user.is_admin == True):
            in_name = request.GET.get('name', 'None')
            in_university = models.University.objects.get(name__exact=in_name)
            in_university.members.add(request.user)
            in_university.save();

            if request.user.is_student == True:
                student = request.user.student
                student.university = in_university
                student.save()
            elif request.user.is_teacher == True:
                teacher = request.user.teacher
                teacher.university = in_university
                teacher.save()
            context = {
                'university' : in_university,
                'userIsMember': True,
            }
            return render(request, 'university.html', context)
        else:
            return render(request, 'baseerror.html', { "message": "You cannot join a university." })
    return render(request, 'autherror.html')
    
def unjoinUniversity(request):
    if request.user.is_authenticated():
        if (request.user.is_student == True or request.user.is_teacher == True or request.user.is_admin == True):
            in_name = request.GET.get('name', 'None')
            in_university = models.University.objects.get(name__exact=in_name)
            in_university.members.remove(request.user)
            in_university.save();

            if request.user.is_student == True:
                student = request.user.student
                student.university = None
                student.save()
            elif request.user.is_teacher == True:
                teacher = request.user.teacher
                teacher.university = None
                teacher.save()
            context = {
                'university' : in_university,
                'userIsMember': False,
            }
            return render(request, 'university.html', context)
        else:
            return render(request, 'baseerror.html', { "message": "You cannot perform this action." })
    return render(request, 'autherror.html')
    
def getCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_member = in_course.members.filter(email__exact=request.user.email)
        is_owner = True if request.user.is_teacher == True and is_member is not None else False

        context = {
            'university': in_university,
            'course': in_course,
            'userInCourse': is_member,
            'is_owner': is_owner
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def courseForm(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        context = {
            'university': in_university,
        }
        return render(request, 'courseform.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def addCourse(request):
    if request.user.is_authenticated():
        if request.user.is_teacher == True or request.user.is_admin == True:
            if request.method == 'POST':
                form = forms.CourseForm(request.POST)
                if form.is_valid():
                    in_university_name = request.GET.get('name', 'None')
                    in_university = models.University.objects.get(name__exact=in_university_name)
                    if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
                        return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
                    new_course = models.Course(tag=form.cleaned_data['tag'],
                                               name=form.cleaned_data['name'],
                                               description=form.cleaned_data['description'],
                                               university=in_university)
                    new_course.save()
                    in_university.course_set.add(new_course)
                    is_member = in_university.members.filter(email__exact=request.user.email)
                    context = {
                        'university' : in_university,
                        'userIsMember': is_member,
                        'user': request.user
                    }
                    return render(request, 'university.html', context)
                else:
                    return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
            else:
                form = forms.CourseForm()
                return render(request, 'courseform.html')
            # render error page if user is not logged in
        else:
            render(request, 'baseerror.html', { "message": "Only teachers can create courses." })
    return render(request, 'autherror.html')
        
def removeCourse(request):
    if request.user.is_authenticated():
        if request.user.is_teacher == True or request.user.is_admin == True:
            in_university_name = request.GET.get('name', 'None')
            in_university = models.University.objects.get(name__exact=in_university_name)
            in_course_tag = request.GET.get('course', 'None')
            in_course = in_university.course_set.get(tag__exact=in_course_tag)
            in_course.delete()
            is_member = in_university.members.filter(email__exact=request.user.email)
            context = {
                'university' : in_university,
                'userIsMember' : is_member,
            }
            return render(request, 'university.html', context)
        else:
            return render(request, 'baseerror.html', { "message": "You do not have permission to remove this course." })
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinCourse(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_teacher == True or request.user.is_admin == True:
            in_university_name = request.GET.get('name', 'None')
            in_university = models.University.objects.get(name__exact=in_university_name)
            in_course_tag = request.GET.get('course', 'None')
            in_course = in_university.course_set.get(tag__exact=in_course_tag)
            in_course.members.add(request.user)
            in_course.save();

            is_member = in_course.members.filter(email__exact=request.user.email)
            is_owner = True if request.user.is_teacher == True and is_member is not None else False

            if request.user.is_student == True:
                request.user.student.classes.add(in_course)
                request.user.student.save()
            elif request.user.is_teacher == True:
                request.user.teacher.classes.add(in_course)
                request.user.teacher.save()

            context = {
                'university' : in_university,
                'course' : in_course,
                'userInCourse': True,
                'is_owner': is_owner
            }
            return render(request, 'course.html', context)
        else:
            return render(request, 'baseerror.html',  { "message": "You do not have permission to join courses." })
    return render(request, 'autherror.html')

def unjoinCourse(request):
    if request.user.is_authenticated():
        if request.user.is_student == True or request.user.is_teacher == True or request.user.is_admin == True:
            user_id = request.GET.get('id', 'None')
            user = None
            userInCourse = True

            try:
                user = MyUser.objects.filter(id=user_id)[0]
            except:
                user = request.user
                userInCourse = False
            
            if request.user.is_teacher == True:
                in_university_name = request.GET.get('name', 'None')
                in_university = models.University.objects.get(name__exact=in_university_name)
                in_course_tag = request.GET.get('course', 'None')
                in_course = in_university.course_set.get(tag__exact=in_course_tag)
                in_course.members.remove(user)
                in_course.save();

                is_member = in_course.members.filter(email__exact=request.user.email)
                is_owner = True if request.user.is_teacher == True and is_member is not None else False
                
                if user.is_student == True:
                    user.student.classes.remove(in_course)
                    user.student.save()
                elif user.is_teacher == True:
                    user.teacher.classes.remove(in_course)
                    user.teacher.save()

                context = {
                    'university' : in_university,
                    'course' : in_course,
                    'userInCourse': userInCourse,
                    'is_owner': is_owner
                }
                return render(request, 'course.html', context)
            else:
                return render(request, 'baseerror.html', { "message": "You do not have permission to remove students from courses." })
        else:
            return render(request, 'baseerror.html',  { "message": "You do not have permission to join courses." })
    return render(request, 'autherror.html')

def getCourseAddStudentForm(request):
    if request.user.is_authenticated():
        if request.user.is_teacher == True or request.user.is_admin == True:
            course_tag = request.GET.get('tag', 'None')
            course = models.Course.objects.get(tag__exact=course_tag)
            is_member = course.members.filter(email__exact=request.user.email)

            if not is_member:
                return render(request, 'baseerror.html', { "message": "Only teachers of this group can add members." })
            else:
                context = {
                    'tag': request.GET.get('tag', 'None'),
                }
                return render(request, 'courseaddstudentform.html', context)
        else:
            return render(request, 'baseerror.html', { "message": "You do not have permission to add members." })   
    return render(request, 'autherror.html')

def getCourseAddStudentFormSuccess(request):
    if request.user.is_authenticated():
        if request.user.is_teacher == True or request.user.is_admin == True:
            if request.method == 'POST':
                form = forms.CourseAddStudentForm(request.POST)
                if form.is_valid():
                    course_to_join = models.Course.objects.get(tag__exact=form.cleaned_data['tag'])

                    try:
                        user = models.MyUser.objects.get(email__exact=form.cleaned_data['email'])
                        course_to_join.members.add(user)
                        course_to_join.save()
                        user.student.classes.add(course_to_join)
                        user.student.save()
                        context = {
                            'tag': course_to_join.tag,
                            'university_name': course_to_join.university.name,
                            'email': form.cleaned_data['email'],
                            'is_owner': True
                        }
                        return render(request, 'courseaddstudentformsuccess.html', context)
                    except ObjectDoesNotExist:
                        return render(request, 'courseaddstudentform.html', { 'error': 'Error: That user does not exist!' })
            else:
                form = forms.GroupForm()
            return render(request, 'courseaddstudentform.html')
        else:
            return render(request, 'baseerror.html', { "message": "You do not have permission to add students." })
    # render error page if user is not logged in
    return render(request, 'autherror.html')
