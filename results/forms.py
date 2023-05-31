from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Sport_competition, Student
from django.contrib.auth.models import User



import re

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()
    

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class StudentRegistrationForm(forms.ModelForm):
    surname = forms.CharField()
    name = forms.CharField()
    patronymic = forms.CharField()
    date = forms.DateField()
    organization = forms.CharField()
    gender = forms.CharField()
    faculty = forms.CharField()
    

    class Meta:
        model = Student
        fields = ('cours',)

        def get_course(self):
            cours=self.cleaned_data['cours']
            return int(cours)



class EnterResults(forms.Form):
    result_sport_competition = forms.CharField()
    name_sport_competition = forms.CharField()
    
    
    def clean_not_template_data(self):
        value = self.cleaned_data['result_sport_competition']
        r_f_t= get_object_or_404(Sport_competition, name_sport_competition = self.cleaned_data['name_sport_competition'])
        reg_exp = r'{}'.format(r_f_t.record_format_template)

        if re.findall(reg_exp, value) or value=='0':
            return value
        else:
            raise ValidationError('Проверьте корректность введённых данных')

class NameSportCompetition(forms.Form):
    name_sport_competition = forms.CharField()

    def get_name_sport_competition(self):
        value=self.data['name_sport_competition']
        return value


        