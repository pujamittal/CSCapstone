"""GroupsApp Models

Created by Naman Patwari on 10/10/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser
from ProjectsApp.models import Project
from ckeditor.fields import RichTextField

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(MyUser)
    project = models.ForeignKey(Project, related_name="project", null=True)


    def __str__(self):
        return self.name
    def get_best_member_skill(self):
        skills = []
        for x in self.members.all():
            if(x.student.skills != None):
                for s in x.student.skills.split(','):
                    skills.append(s)
        return max(set(skills), key=skills.count)

class GroupComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment = RichTextField(config_name='awesome_ckeditor')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name