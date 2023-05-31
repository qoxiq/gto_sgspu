
from copyreg import dispatch_table
from distutils.log import error
from logging import raiseExceptions
from multiprocessing import context
from urllib import request
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

import results
from .models import Student, Results_sport_competition, Sport_competition, Organization, Faculty, Instructor
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import EnterResults, UserRegistrationForm, StudentRegistrationForm, NameSportCompetition
import datetime
from django.views import generic
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
import json
import re
import logging



logger = logging.getLogger(__name__)

# Create your views here.
class ResultsListView(generic.ListView):
    
    def get_queryset(self):
        user = User.objects.filter(id=self.request.user.id)[0]
        if user.groups.filter(name='Students').count():
            students = Student.objects.filter(t_user = user)
        else:
            uin=self.request.GET.get('id')
            students = Student.objects.filter(uin_user = uin)
        return Results_sport_competition.objects.filter(id_user = students[0]) 
    

    #model = Results_sport_competition
    context_object_name = 'user_results_list'   # ваше собственное имя переменной контекста в шаблоне
    #student=get_queryset
    #queryset = Results_sport_competition.objects.filter(id_user = student)
    logging.error('error')
    template_name = 'results/viewResults.html'  # Определение имени вашего шаблона и его расположения


def main(request):
    return render(request, 'results/main.html')

def history(request):
    return render(request, 'results/history.html')

def standards(request):
    return render(request, 'results/standards.html')

def contacts(request):
    return render(request, 'results/contacts.html')

def studentsPersonal(request):
    return render(request, 'results/studentsPersonal.html')

def standardsPersonal(request):
    return render(request, 'results/standardsPersonal.html')


def registration(request):
    if request.method == 'POST':
        print('1')
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST)
        print(user_form)
        if user_form.is_valid() and student_form.is_valid():
            print('2')
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            new_user.groups.add(Group.objects.get(name='Students'))
            if not re.findall(r'^\d{2}-\d{2}-\d{7}$', new_user.username):
                new_user.delete()
                user_form = UserRegistrationForm()
                student_form = StudentRegistrationForm()
                return render(request, 'results/registration.html', {'user_form': user_form, 'studend_form': student_form})
                
            new_student = student_form.save(commit=False)
            new_student.t_user=new_user
            new_student.uin_user=new_user.username
            new_student.fio_user=student_form.cleaned_data['surname']+' '+student_form.cleaned_data['name']+' '+student_form.cleaned_data['patronymic']
            new_student.date_of_birth=student_form.cleaned_data['date']

            if(student_form.cleaned_data['gender']=='Мужской'):
                new_student.gender=1
            else:
                new_student.gender=0
                
            organization=get_object_or_404(Organization, short_name_organization = student_form.cleaned_data['organization'])
            new_student.organization_id=organization

            faculty=get_object_or_404(Faculty, short_name_faculty = student_form.cleaned_data['faculty'])
            new_student.faculty_id=faculty
            new_student.cours=student_form.cleaned_data['cours']
            new_student.group='-'
            new_student.consept_personal_data=True
            new_student.medal_gto='Нет'
            new_student.stage_gto=6
            new_student.additional_information='Нет дополнительной информации'
            new_student.save()

            return render(request, 'results/registration_done.html', {'new_user': new_user})      
    else:
        user_form = UserRegistrationForm()
        student_form = StudentRegistrationForm()
    return render(request, 'results/registration.html', {'user_form': user_form, 'studend_form': student_form})



def profile(request):
    user = get_object_or_404(Student, uin_user = request.user.username)
    fio_arr=user.fio_user.split()
    context = {
             'fio_user' : user.fio_user,
             'f_user' : fio_arr[0],
             'i_user' : fio_arr[1],
             'o_user' : fio_arr[2],
             'uin_user' : user.uin_user,
             'date_of_birth' : user.date_of_birth,
             'gender' : user.gender,
             'organization_short_name' : user.organization_id,
             'faculty_short_name' : user.faculty_id,
             'group' : user.group,
             'cours' : user.cours,
             'consept_personal_data' : user.consept_personal_data,
             'medal_gto' : user.medal_gto,
             'stage_gto' : user.stage_gto,
             'additional_information' : user.additional_information,
             'role' : user.__class__.__name__
         }

    return render(request, 'results/profile.html', context)

    

def enterResults(request):
    new_result=Results_sport_competition()
#НЕ РАБОТАЕТ
    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = EnterResults(request.POST)
        print(form.is_valid())
        print(form.cleaned_data['result_sport_competition'])
        print(form.cleaned_data['name_sport_competition'])
        
        

        # Проверка валидности данных формы:
        if form.is_valid() and form.clean_not_template_data()==form.cleaned_data['result_sport_competition']:
            
            sport_competition = get_object_or_404(Sport_competition, name_sport_competition = form.cleaned_data['name_sport_competition'])
            print('2')
            student = get_object_or_404(Student, uin_user = request.user.username)
            print('3')
            new_result.results_sport_competition = form.cleaned_data['result_sport_competition']
            print('4')
            new_result.id_user=student
            print('5')
            new_result.id_sport_competition = sport_competition
            print('6')
            new_result.date = datetime.date.today()
            new_result.number_of_try = 1
            new_result.accepted = False
            new_result.save()
            print('save')
            return render(request, 'results/enterResults.html', {'form': form})
            #return HttpResponseRedirect(reverse('enterResults') )
        else:
            print('error')
            error_message="Проверьте корректность введённых данных"
            form = EnterResults(initial={'result_sport_competition': error_message})
            return render(request, 'results/enterResults.html', {'form': form})
        
    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        sport_competitions = Sport_competition.objects.all()
        names_sport_competitions_list=[]
        
        for elem in sport_competitions:
            names_sport_competitions_list.append(elem.name_sport_competition+' ('+elem.units+')')
        names_sport_competitions_list.sort()
        

        form = EnterResults(initial={'names_sport_competitions_list': names_sport_competitions_list.sort(),})

    return render(request, 'results/enterResults.html', {'form': form, 'newresult':new_result})

def checkPermission(request):
    user = get_object_or_404(User, username = request.user.username)
    if user.groups.filter(name='Students').count():
        #return HttpResponse('Ошибка доступа')
        return redirect('/results/studentsPersonal') #studentsPersonal(request)
    elif user.groups.filter(name='Instructors').count():
       return redirect('/results/teacherPersonal')
    else:
        return HttpResponse('Ошибка доступа')
    
def teacherPersonal(request):
    if request.user.groups.filter(name='Instructors').count():
        return render(request, 'results/teacherPersonal.html')
    else:
        return HttpResponse('Ошибка доступа')

def standardsPersonalTeacher(request):
    return render(request, 'results/standardsPersonalTeacher.html')

def profileTeacher(request):
    instructor = get_object_or_404(Instructor, t_user = request.user)
    fio_arr=instructor.fio_instructor.split()
    context = {
             'fio_user' : instructor.fio_instructor,
             'f_user' : fio_arr[0],
             'i_user' : fio_arr[1],
             'o_user' : fio_arr[2],
             'organization_short_name' : instructor.organization_id,
             'phone_instructor' : instructor.phone_instructor,
             'mail' : instructor.mail_instructor,
             'role' : instructor.__class__.__name__
         }

    return render(request, 'results/profileTeacher.html', context)


def create_dict_students_scores():

    logs_female = open('logs_female.txt', 'w')
    logs_male = open('logs_male.txt', 'w')
    female_score={} #очки хранятся в словаре в виде 'УИН'-'количество очков
    male_score={}

    female_list=Student.objects.filter(gender=0)
    for elem in female_list:
        female_score[elem.uin_user]=0

    male_list=Student.objects.filter(gender=1)
    for elem in male_list:
        male_score[elem.uin_user]=0
    
    competitions_list=get_list_or_404(Sport_competition)

    for competition in competitions_list:
        result_competition_list=list(Results_sport_competition.objects.filter(id_sport_competition = competition))
        if type(result_competition_list)!=type(None) and len(result_competition_list)!=0:
            female_result_competition_list=[]
            male_result_competition_list=[]
            if result_competition_list[0].id_sport_competition.name_sport_competition == 'Плавание на 50 м' :
                result_competition_list.sort(key=lambda x: x.results_sport_competition)
            else:
                result_competition_list.sort(key=lambda x: float(x.results_sport_competition.replace(',', '.')), reverse=True)
            for i in range(len(result_competition_list)):
                if result_competition_list[i].id_user.gender==0:
                    female_result_competition_list.append(result_competition_list[i])
                else:
                    male_result_competition_list.append(result_competition_list[i])

        #сперва добавляем баллы студентам, сдавших норматив
            
            score=len(female_result_competition_list)
            for i in range(len(female_result_competition_list)):
                if i == 0:
                    female_score[female_result_competition_list[i].id_user.uin_user] = female_score[female_result_competition_list[i].id_user.uin_user] + score
                else:
                    if female_result_competition_list[i].results_sport_competition != female_result_competition_list[i-1].results_sport_competition:
                        score=score-1
                    female_score[female_result_competition_list[i].id_user.uin_user] = female_score[female_result_competition_list[i].id_user.uin_user] + score
                logs_female.write(str(female_result_competition_list[i].id_user. fio_user)+'  '+str(female_result_competition_list[i].id_sport_competition.name_sport_competition)+'  '+str(female_result_competition_list[i].results_sport_competition)+'  ')
                logs_female.write(str(score)+'\n')


            
            score=len(male_result_competition_list)
            for i in range(len(male_result_competition_list)):
                
                if i == 0:
                    male_score[male_result_competition_list[i].id_user.uin_user] = male_score[male_result_competition_list[i].id_user.uin_user] + score
                else:
                    if male_result_competition_list[i].results_sport_competition != male_result_competition_list[i-1].results_sport_competition:
                        score=score-1
                    male_score[male_result_competition_list[i].id_user.uin_user] = male_score[male_result_competition_list[i].id_user.uin_user] + score
                logs_male.write(str(male_result_competition_list[i].id_user. fio_user)+'  '+str(male_result_competition_list[i].id_sport_competition.name_sport_competition)+'  '+str(male_result_competition_list[i].results_sport_competition)+'  ')
                logs_male.write(str(score)+'\n')
            

    
    sorted_female_score = dict(sorted(female_score.items(), key=lambda item: item[1], reverse=True))
    sorted_male_score = dict(sorted(male_score.items(), key=lambda item: item[1], reverse=True))
    #Удаляем пользователей с нулевыми баллами из словаря
    keys_female=list(sorted_female_score.keys())
    values_female=list(sorted_female_score.values())

    for i in range(len(keys_female)):
        if values_female[i]==0:
            sorted_female_score.pop(keys_female[i])

    keys_male=list(sorted_male_score.keys())
    values_male=list(sorted_male_score.values())

    for i in range(len(keys_male)):
        if values_male[i]==0:
            sorted_male_score.pop(keys_male[i])


    context={'female':sorted_female_score,
             'male':sorted_male_score}

    logs_female.close()
    logs_male.close()

    return context


def winner_individual(request):
    context=create_dict_students_scores()

    sorted_female_score=context['female']
    sorted_male_score=context['male']
    uin_female=list(sorted_female_score.keys())
    uin_male=list(sorted_male_score.keys())
    
    output_dict_male={}
    output_dict_female={}
    
    size_dict_famale=len(uin_female)
    size_dict_male=len(uin_male)
    
    place = 1
    for elem in uin_female[:size_dict_famale]:
        student=get_object_or_404(Student, uin_user=elem)
        row=[place, student.fio_user, elem, sorted_female_score[elem]]
        place = place + 1
        output_dict_female[elem] = row

    place=1
    for elem in uin_male[:size_dict_male]:
        student = get_object_or_404(Student, uin_user=elem)
        row = [place, student.fio_user, elem, sorted_male_score[elem]]
        place=place+1
        output_dict_male[elem]=row

    with open("INDIVIDUAL_RESULTS_FEMALE.txt", "w") as file:
        json.dump(sorted_female_score, file)

    with open("INDIVIDUAL_RESULTS_MALE.txt", "w") as file:
        json.dump(sorted_male_score, file)

    context={
        'female':output_dict_female,
        'male':output_dict_male
    }

    return render(request, 'results/individualWinner.html', context)
    #return JsonResponse(context)

#-----------------------------------------------------------
    # keys=list(sorted_score.keys())
    # values=list(sorted_score.values())
    # for i in range(len(keys)):
    #     res=res+keys[i]+'  '+str(values[i])+'\n'
    

def winner_team(request):
    score={} #очки хранятся в словаре в виде 'НАЗВАНИЕ КОМАНДЫ'-'количество очков'
    dict_students_scores=create_dict_students_scores()
    union_scores=dict_students_scores['female']|dict_students_scores['male']
    teams_list=get_list_or_404(Faculty)
    
    for team in teams_list:
        score[team.full_name_faculty]=0
    
    for uin,value in union_scores.items():
        student=Student.objects.filter(uin_user=uin)[0]
        score[student.faculty_id.full_name_faculty] = score[student.faculty_id.full_name_faculty] + int(value)

        
      
    sorted_score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))
    team_name_list=list(sorted_score.keys())
    team_score_list=list(sorted_score.values())

    for i in range(len(team_name_list)):
        if team_score_list[i]==0:
            sorted_score.pop(team_name_list[i])

    output_dict={}
    place = 1
    for team_name, team_score in sorted_score.items():
        row=[place, team_name, team_score]
        place = place + 1
        output_dict[team_name] = row

    context={
        'context':output_dict,
    }
    
    with open('TEAM_RESULTS.txt', 'w') as file:
        file.write('<Название фикультета> - <количество очков>\n')
        for key, value in sorted_score.items():
            file.write(f'{key} - {value}\n')
    #with open("TEAM_RESULTS.txt", "w", encoding='utf-8') as file:
        #json.dump(sorted_score,  file)
        

    return render(request, 'results/teamWinner.html', context)
    #return JsonResponse(context)

def orgEnterResults(request):
    
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        # if request.POST.get("name_sport_competition").count('(') == 1:
        #     name_sport_competition=request.POST.get("name_sport_competition").split(' (')[0]
        # else:
        #     name_sport_competition=str(request.POST.get("name_sport_competition").split(' (')[0])+' ('+str(request.POST.get("name_sport_competition").split(' (')[1])
        name_sport_competition=request.POST.get("name_sport_competition")
        logger.error(name_sport_competition)
        sport_competition = get_object_or_404(Sport_competition, name_sport_competition =  name_sport_competition)
        student = get_object_or_404(Student, uin_user = request.POST.get("uin"))
        new_result=Results_sport_competition()
        result_sport_competition=request.POST.get("result_sport_competition")
        new_result.results_sport_competition = result_sport_competition
        new_result.id_user=student
        new_result.id_sport_competition = sport_competition
        new_result.date = datetime.date.today()
        new_result.number_of_try = 2
        new_result.accepted = False
        new_result.save()
        return HttpResponse('ok')
        

    else:
        students_dict={}
        students=list(Student.objects.all())
        if students:
            for student in students:
                students_dict[student.uin_user]=student.fio_user
        sorted_students_dict = dict(sorted(students_dict.items(), key=lambda item: item[0]))
        form = EnterResults()
                    
       # context={'students' : sorted_students_dict}
        return render(request, 'results/orgEnteringResults.html', {'form': form, 'students' : sorted_students_dict})

def protocol(request):
    if request.method == 'POST':
        form = NameSportCompetition(request.POST)
        results_sport_competition_dict={}
        name_sport_competition=form.get_name_sport_competition()
        print(name_sport_competition)
        sport_competition=get_object_or_404(Sport_competition, name_sport_competition =  name_sport_competition)
        results_sport_competition_list = list(Results_sport_competition.objects.filter(id_sport_competition=sport_competition))
        results_sport_competition_list.sort(key=lambda x: float(x.results_sport_competition.replace(',', '.')), reverse=True)
        #№    Ф.И.О.     УИН участника       пол    факультет     курс      ступень ГТО      результат выполнения             уровень выполнения
        for i in range(1, len(results_sport_competition_list)):
            
            row={}
            row['FIO'] = results_sport_competition_list[i].id_user.fio_user # ФИО
            row['UIN'] = results_sport_competition_list[i].id_user.uin_user # УИН
            if results_sport_competition_list[i].id_user.gender==0: # ПОЛ
                row['GENDER'] = 'женский'
            else:
                row['GENDER'] = 'мужской'
            row['FACULTY'] = results_sport_competition_list[i].id_user.faculty_id.short_name_faculty # факультет
            row['COURS'] = str(results_sport_competition_list[i].id_user.cours) # курс
            row['STAGE_GTO'] = str(results_sport_competition_list[i].id_user.stage_gto) # ступень ГТО
            row['RESULT_SPORT_COMPETITION'] = str(results_sport_competition_list[i].results_sport_competition) # результат выполнения
            row['LVL_RESULT'] = '-' # уровень выполнения
            #row.append(results_sport_competition_list[i].id_sport_competition.name_sport_competition)
            results_sport_competition_dict[str(i)] = row
            context={
                'results_sport_competition_dict' : results_sport_competition_dict
                }
            print(context)

        #return HttpResponse(context)
        return render(request, 'results/protocol.html', {'form' : form, 'results_sport_competition_dict' : results_sport_competition_dict, 'name_sport_competition' : name_sport_competition})
    else:
        form=NameSportCompetition()
        results_sport_competition_dict={}
        name_sport_competition=''
        return render(request, 'results/protocol.html', {'form' : form, 'results_sport_competition_dict' : results_sport_competition_dict })
# def protocol(request):
#     if request.method == 'POST':
#         form = NameSportCompetition(request.POST)
#         results_sport_competition_dict={}
#         name_sport_competition=form.get_name_sport_competition()
#         print(name_sport_competition)
#         sport_competition=get_object_or_404(Sport_competition, name_sport_competition =  name_sport_competition)
#         results_sport_competition_list = list(Results_sport_competition.objects.filter(id_sport_competition=sport_competition))
#         results_sport_competition_list.sort(key=lambda x: float(x.results_sport_competition.replace(',', '.')), reverse=True)
#         #№    Ф.И.О.     УИН участника       пол    факультет     курс      ступень ГТО      результат выполнения             уровень выполнения
#         for i in range(1, len(results_sport_competition_list)):
            
#             row=[]
#             row.append(results_sport_competition_list[i].id_user.fio_user) # ФИО
#             row.append(results_sport_competition_list[i].id_user.uin_user) # УИН
#             if results_sport_competition_list[i].id_user.gender==0: # ПОЛ
#                 row.append('женский')
#             else:
#                 row.append('мужской')
#             row.append(results_sport_competition_list[i].id_user.faculty_id.short_name_faculty) # факультет
#             row.append(str(results_sport_competition_list[i].id_user.cours)) # курс
#             row.append(str(results_sport_competition_list[i].id_user.stage_gto)) # ступень ГТО
#             row.append(str(results_sport_competition_list[i].results_sport_competition)) # результат выполнения
#             row.append('-') # уровень выполнения
#             #row.append(results_sport_competition_list[i].id_sport_competition.name_sport_competition)
#             results_sport_competition_dict[str(i)] = row
#             context={
#                 'results_sport_competition_dict' : results_sport_competition_dict
#                 }

#         #return HttpResponse(context)
#         return render(request, 'results/protocol.html', {'form' : form, 'results_sport_competition_dict' : results_sport_competition_dict, 'name_sport_competition' : name_sport_competition})
#     else:
#         form=NameSportCompetition()
#         results_sport_competition_dict={}
#         name_sport_competition=''
#         return render(request, 'results/protocol.html', {'form' : form, 'results_sport_competition_dict' : results_sport_competition_dict })

def summaryProtocol(request):
    names_sport_competitons_list=list(Sport_competition.objects.all())
    names_sport_competitons_list.sort(key=lambda x: x.name_sport_competition, reverse=False)

    students=list(Student.objects.all())
    data=[]
    for student in students:
        row=[]
        #row.append(datetime.datetime.now)
        row.append(student.fio_user)
        row.append(student.faculty_id.short_name_faculty+', '+str(student.cours)+' курс')
        row.append(student.uin_user)
        for name_sport_competition in names_sport_competitons_list:
            result_sport_competition=Results_sport_competition.objects.filter(id_sport_competition =  name_sport_competition, id_user =  student)
            logging.error(type(result_sport_competition))
            if len(result_sport_competition) != 0:
                row.append(result_sport_competition[0].results_sport_competition)
            else:
                row.append('-')
        data.append(row)
    context={
           'names_sport_competitons_list' : names_sport_competitons_list,
           'data' : data, 
    }
    #return HttpResponse(TYPES)
    return render(request, 'results/summaryProtocol.html', context = context)