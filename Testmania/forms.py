from django import forms
from .models import Contests,Questions,Profile
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


inputDateFormat=[   '%Y-%m-%d',      # 2006-10-25
                    '%m/%d/%Y',       #10/25/2006
                    '%m/%d/%y']       # 10/25/06
class inputDate(forms.DateInput):
    input_type='date'
class inputTime(forms.TimeInput):
    input_type='time'

class registerForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password']


class loginForm(forms.Form):
    username=forms.CharField(max_length=15,required=True)
    password=forms.CharField(max_length=15,required=True)


class createTestModelForm(forms.ModelForm):
    class Meta:
        model=Contests
        fields=['contest','noOfQues','startDate','startTime','endDate','endTime','timePerQues']
        widgets={
            'startDate':inputDate(),
            'endDate':inputDate(),
            'startTime':inputTime(),
            'endTime':inputTime(),
            }
        labels={
            'contest':'Test Name',
            'noOfQues':'Number of questions',
            'timePerQues':'Time per questions(in seconds)',
            'startDate':'Start date of test',
            'startTime':'Start time of test',
            'endDate':'End date of test',
            'endTime':'End time of test',
            }
        help_texts={
            'timePerQues':'In seconds (e.g. 60 for 1 minute)',
        }

class createQuestionModelForm(forms.ModelForm):
    class Meta:
        model=Questions
        fields=['question','optionA','optionB','optionC','optionD','answer']
        widgets={
            'question':forms.Textarea(attrs={"rows":"3"})
        }
        
class updateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model=Profile
        fields=['Profile_pic','Roll_no','Branch']

        
    