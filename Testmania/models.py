from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
def get_profile_path(instance,fileName):
    return "images/{username}/{fileName}".format(username=instance.user.id,fileName=fileName)
class Contests(models.Model):
    contest=models.CharField(max_length=100, unique=True)
    Author=models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    noOfQues=models.IntegerField()
    startDate=models.DateField()
    startTime=models.TimeField()
    endDate=models.DateField()
    endTime=models.TimeField()
    timePerQues=models.CharField(max_length=12)
    participants=models.ManyToManyField(User,related_name="contest_participants")
    isEditorsChoice=models.BooleanField(default=False)

class Profile(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    Profile_pic=models.ImageField(upload_to=get_profile_path,default='images/default-user-icon.jpg')
    Roll_no=models.IntegerField(blank=True,null=True,default=None)
    Branch=models.CharField(blank=True,null=True,max_length=50,default=None)

class Questions(models.Model):
    answerChoices=[
        ('A','Option A'),
        ('B','Option B'),
        ('C','Option C'),
        ('D','Option D'),
    ]
    question=models.CharField(blank=True,max_length=200,default=None)
    optionA=models.CharField(blank=True,max_length=50,default=None)
    optionB=models.CharField(blank=True,max_length=50,default=None)
    optionC=models.CharField(blank=True,max_length=50,default=None)
    optionD=models.CharField(blank=True,max_length=50,default=None)
    contest=models.ForeignKey(Contests,on_delete=models.CASCADE)
    answer=models.CharField(choices=answerChoices, blank=True,max_length=5,default=None)
    responseA=models.ManyToManyField(User,related_name="response_a")
    responseB=models.ManyToManyField(User,related_name="response_b") 
    responseC=models.ManyToManyField(User,related_name="response_c") 
    responseD=models.ManyToManyField(User,related_name="response_d")
    participants=models.ManyToManyField(User,related_name="participants")

admin.site.register(Contests)
admin.site.register(Questions)
admin.site.register(Profile)

