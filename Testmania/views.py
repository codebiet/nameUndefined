from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import registerForm,loginForm,createTestModelForm,createQuestionModelForm,updateProfileForm
from .models import Contests,Questions,Profile
from random import randint
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import ValidationError
from datetime import datetime
#To display Home Page
def homePage(request):
    auth=False
    if request.user.is_authenticated:
        auth=True
    return render(request,'index.html',{'a':auth,'username':request.user.username,'info':"in the home page"})

# To display Registration Page
def registerView(request):
    if request.user.is_authenticated:
        messages.info(request,"You are already registered")
        return redirect("/")
    if request.method=="POST":
        form=registerForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            profile=Profile.objects.create(user=user)
            profile.save
            login(request,user)
            messages.success(request,"welcome {username}! You're successfully registered.".format(username=user.username))
            return redirect('/',{'info':"Registration Successful"})
        else:
            return render(request,'register.html',{'form':form})
    else:
        form=registerForm()
        return render(request,'register.html',{'form':form})

#To display login Page
def loginView(request):
    if request.user.is_authenticated:
        messages.info(request,"You're already in.")
        return redirect("/")
    if request.method=="POST":
        form=loginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,
            password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"welcome {username}".format(username=user.username))
                return redirect("/")
            else:
                form.add_error(None,"incorrect username or password")
                return render(request,"login.html",{"form":form,"info":"incorrect username or password"})
        else:
            return render(request,"login.html",{"form":form,"info":"login failed due to form is not valid"})
    else:
        form=loginForm()
        return render(request,"login.html",{"form":form,"info":"please input the details to login"})


#To display logout Page
@login_required
def logoutView(request):
    logout(request)
    return redirect('/')


#To display create test Page
@login_required
def createTestView(request):
    if request.method=="POST":
        form=createTestModelForm(request.POST)
        if form.is_valid():
            contest=form.save(commit=False)
            contest.Author=request.user
            contest.save()
            form=createQuestionModelForm()
            return render(request,"createQuestion.html",{'form':form,'noOfQues':contest.noOfQues,"qNo":1,'contestId':contest.id,'a':True,'username':request.user.username})
        else:
            messages.error(request,"failed with some internal error")

            return redirect("/")
    else:
        form=createTestModelForm()
        return render(request,"createTest.html",{'form':form,'a':True,'username':request.user.username})


#To display take test Page
@login_required
def takeTestView(request):
    
    if request.method=='POST':
        id=request.POST.get('id')
        query_set=Contests.objects.filter(pk=id)
        if query_set.count()>0:
            questDetail=displayUtil(request,query_set[0])
            if questDetail is None:
                messages.success(request,"You have completed this test. please proceed to test taken section to see result")

                return redirect('/dashboard/')
            questDetail.update(getUser(request))
            query_set[0].participants.add(request.user)
            return render(request,"displayQuestion.html",questDetail)
        else:
            messages.error(request,"Requested contest doesn't exist")
            return redirect("/taketest/")
    else:
        messages.info(request,"Please ask contest id by the author of the test.")
        form={"onGoingContest":ongoingContestsUtil(request)}
        return render(request,'takeTest.html',form)
    
    
#for create Question Page
@login_required
def createQuestionView(request):
    contestId=request.POST.get("contestId")
    contest=Contests.objects.get(pk=contestId)
    if contestId is None:
        redirect('/')
    if request.user is not contest.Author:
        redirect('/')
    
    if request.method=="POST":
        form=createQuestionModelForm(request.POST)
        ques=form.save(commit=False)
        ques.contest=contest
        ques.save()



        qNo=int(request.POST.get("qNo"))+1
        form=createQuestionModelForm()

        if qNo > contest.noOfQues:
            messages.success(request,"Thanks for creating the contest. Please proceed to dashboard for other info")

            return redirect("/")
        return render(request,"createQuestion.html",{'form':form,'noOfQues':contest.noOfQues,"qNo":qNo,'contestId':contest.id,'a':True,'username':request.user.username})
    else:
        form=createQuestionModelForm()
        return render(request,"createQuestion.html",{'form':form,'noOfQues':contest.noOfQues,"qNo":1,'contestId':contest.id,'a':True,'username':request.user.username})
@login_required
def profileView(request):
    if request.method=='POST':
        try:
            form=updateProfileForm(request.POST,request.FILES,instance=request.user.profile)
            form.save()
        except:
            form=updateProfileForm(request.POST,request.FILES)
            profile=form.save()
            profile.user=request.user
            profile.save()
        return redirect('/')
    else:
        form=updateProfileForm()
        return render(request,'profile.html',{'form':form,'a':True,'username':request.user.username})
#for display questions
@login_required
def displayQuesView(request):
    if request.method=="POST":
        quesId=request.POST.get('quesId')
        contestId=request.POST.get('contestId')
        option=request.POST.get('option')
        q=Questions.objects.get(pk=quesId)
        if option=='A':
            q.responseA.add(request.user)
        elif option=='B':
            q.responseB.add(request.user)
        elif option=='C':
            q.responseC.add(request.user)
        else:
            messages.info(request,"Since you haven't provided any option so, option D is set as default")
            q.responseD.add(request.user)
        q.save()
        
        contest=Contests.objects.get(pk=contestId)
        questDetail=displayUtil(request,contest)
        
        if questDetail is None:
            messages.success(request,"Thanks for participating, please proceed to test taken section to check results")
            return redirect("/dashboard/")
        questDetail.update(getUser(request))
        return render(request,"displayQuestion.html",questDetail)


    else:

        return redirect('/taketest/')
        

@login_required
def dashboardView(request):
    form=getUser(request)
    form.update({"contestCreated":contestCreatedDetails(request)})
    form.update({"contestTaken":contestTakenDetails(request)})
    
    values=[]
    obj=request.user
    try:
        pf=obj.profile
        values.append([obj.username,obj.first_name,obj.last_name,obj.email,pf.Branch,pf.Profile_pic,pf.Roll_no]) 
    except:
        values.append([obj.username,obj.first_name,obj.last_name,obj.email,'not provided','default-user-icon.jpg','not provided'])

    form.update({"detail":values})  

    return render(request,"dashboard.html",form)

@login_required
def testTakenDetailView(request,contestId):
    contest=Contests.objects.get(id=contestId)
    user=request.user
    form=getUser(request)
    form.update({"questionDetails":testTakendetailsUtil(contest,user),"contestName":contest.contest})
    return render(request,"testTakendetail.html",form)





def testTakendetailsUtil(contest,user):
    q=Questions.objects.filter(contest=contest)
    questionArray=[]
    counter=1
    for i in q:
        rA=False
        rB=False
        rC=False
        rD=False
        iscorrect=False
        if user in i.responseA.all():
            rA=True

            if i.answer=='A':
                iscorrect=True
        if user in i.responseB.all():
            rB=True
            if i.answer=='B':
                iscorrect=True
        if user in i.responseC.all():
            rC=True
            if i.answer=='C':
                iscorrect=True
        if user in i.responseD.all():
            rD=True
            if i.answer=='D':
                iscorrect=True
        j={"quesNo":counter,
            "isCorrect":iscorrect,
            "name":"ques"+str(i.id),
            "question":i.question,
            "A":i.optionA,
            "B":i.optionB,
            "C":i.optionC,
            "D":i.optionD,
            "responseA":rA,
            "responseB":rB,
            "responseC":rC,
            "responseD":rD,
            "answer":"option"+i.answer,
        }
        counter+=1
        questionArray.append(j)
    return questionArray







#utility function to display a question
def displayUtil(request,contestobj):
    questionSet=Questions.objects.filter(contest=contestobj).exclude(responseA=request.user).exclude(responseB=request.user).exclude(responseC=request.user).exclude(responseD=request.user)
    n=len(questionSet)
    if n==0:
        return None
    index=randint(0,n-1)
    ques=questionSet[index]
    tNo=contestobj.noOfQues
    quesDetail={
        'time':contestobj.timePerQues,
        'contestId':contestobj.id,
        'quesId':ques.id,
        'ques':ques.question,
        'A':ques.optionA,
        'B':ques.optionB,
        'C':ques.optionC,
        'D':ques.optionD,
        'tNo':tNo,
        'quesNo':tNo-n+1
    }
    return quesDetail


def contestCreatedDetails(request):
    user=request.user
    querySet=Contests.objects.filter(Author=user)
    contestArray=[]
    for i in querySet:
        noOfPart=len(i.participants.all())
        td={
            "id":i.id, 
            "contest":i.contest,
            "noOfParticipants":noOfPart,
            "startDate":i.startDate,
            "startTime":i.startTime,
            "endDate":i.endDate,
            "endTime":i.endTime,
    
        }

        contestArray.append(td)

    return contestArray



def contestTakenDetails(request):
    user=request.user
    querySet=Contests.objects.filter(participants=user)
    contestArray=[]
    for i in querySet:
        score=getScore(user,i)
        td={
            "id":i.id,
            "contest":i.contest,
            "score":str(score)+"/"+str(i.noOfQues),
            "startDate":i.startDate,
            "startTime":i.startTime,
            "endDate":i.endDate,
            "endTime":i.endTime,
            }
        contestArray.append(td)

    return contestArray


def getScore(user,contest):
    queryset=Questions.objects.filter(contest=contest)
    score=0
    for i in queryset:
        if i.answer=='A':
            if user in i.responseA.all():
                score+=1
        if i.answer=='B':
            if user in i.responseB.all():
                score+=1   
        if i.answer=='C':
            if user in i.responseC.all():
                score+=1 
        if i.answer=='D':
            if user in i.responseD.all():
                score+=1 
    return score                     
def getUser(request):
    auth=False
    if request.user.is_authenticated:
        auth=True
    return {'a':auth,'username':request.user.username,'info':""}

def contest_records(request,contest_id):
    query=User.objects.filter(contest_participants=contest_id)
    values=[]
    for i in query:
        try:
            obj=i.profile
            values.append([i.username,getScore(i,contest_id),i.email,obj.Branch,obj.Roll_no])
        except:
            values.append([i.username,getScore(i,contest_id),i.email,'You have not provided us yet','You have not provided us yet'])

    return render(request,'contest_records.html',{'participants':values,"a":True,"username":request.user.username})

def ongoingContestsUtil(request):
    currTime=datetime.now().time()
    currDate=datetime.now().date()
    querySet=Contests.objects.filter(startDate__lte=currDate,endDate__gte=currDate).exclude(startDate=currDate,startTime__gt=currTime).exclude(endDate=currDate,endTime__lt=currTime)
    contestArray=[]
    for i in querySet:
        td={
            "id":i.id,
            "contest":i.contest,
            "author":i.Author,
            "startDate":i.startDate,
            "startTime":i.startTime,
            "endDate":i.endDate,
            "endTime":i.endTime,
            }
        contestArray.append(td)

    return contestArray