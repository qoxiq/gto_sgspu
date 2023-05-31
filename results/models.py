
from email.policy import default
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    id_organization = models.PositiveIntegerField(primary_key=True)
    short_name_organization = models.CharField(max_length=15)
    full_name_organization = models.CharField(max_length=200)
    official_phone_organization = models.CharField(max_length=20)
    contact_person_name_organization = models.CharField(max_length=50)
    contact_person_phone_organization = models.CharField(max_length=20)

    def __str__(self):
        return str(self.short_name_organization)

class Faculty(models.Model):
    id_faculty = models.PositiveIntegerField(primary_key = True)
    short_name_faculty = models.CharField(max_length=15)
    full_name_faculty = models.CharField(max_length=200)
    official_phone_faculty = models.CharField(max_length=20)
    contact_person_name_faculty = models.CharField(max_length=50)
    contact_person_phone_faculty = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.short_name_faculty)
    
    
class Sport_competition(models.Model):
    id_sport_competition = models.PositiveIntegerField(primary_key=True)
    name_sport_competition = models.CharField(max_length=200)
    units = models.CharField(max_length=50)
    record_format_template = models.CharField(max_length=500)

    def __str__(self):
        return str(self.name_sport_competition)

class Cathedra(models.Model):
    id_cathedra = models.PositiveIntegerField(primary_key=True)
    short_name_cathedra = models.CharField(max_length=15)
    full_name_cathedra =  models.CharField(max_length=200)

    def __str__(self):
        return str(self.short_name_cathedra)


class Instructor(models.Model):
    t_user=models.OneToOneField(User, on_delete=models.CASCADE)
    fio_instructor = models.CharField(max_length=100)
    mail_instructor = models.CharField(max_length=100)
    phone_instructor = models.CharField(max_length=20)
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE) 
    

    def __str__(self):
        return str(self.fio_instructor)
    
class Student(models.Model):
    GENDERS = [
        (0, 'Женский'),
        (1, 'Мужской')
    ]

    CONSEPT_PERSONAL_DATA = [
        (False, 'Нет'),
        (True, 'Да')
    ]

    MEDAL = [
        ("Золото", 'Золото'),
        ("Серебро", 'Серебро'),
        ("Бронза", 'Бронза'),
        ("Нет", 'Нет'),
    ]
    t_user=models.OneToOneField(User, on_delete=models.CASCADE)
    fio_user = models.CharField(max_length=100)
    uin_user = models.CharField(max_length=13, primary_key=True)
    date_of_birth = models.DateField()
    gender = models.SmallIntegerField(choices = GENDERS)
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    cours = models.PositiveIntegerField()
    group = models.CharField(max_length=50, default='-')
    consept_personal_data=models.BooleanField(choices = CONSEPT_PERSONAL_DATA)
    medal_gto = models.CharField(max_length=15, default = "Нет", choices=MEDAL, blank=False)
    stage_gto = models.PositiveIntegerField()
    additional_information = models.CharField(max_length=255, default = 'Нет дополнительной информации')

    def get_info(self):
        info = {
            'fio_user' : self.fio_user,
            'uin_user' : self.uin_user,
            'date_of_birth' : self.date_of_birth,
            'gender' : self.gender,
            'organization_id' : str(self.organization_id),
            'faculty_id' : str(self.faculty_id),
            'cours' : self.cours,
            'consept_personal_data' : self.consept_personal_data,
            'medal_gto' : self.medal_gto,
            'stage_gto' : self.stage_gto,
            'additional_information' : self.additional_information
        }
        return info

    def __str__(self):
        return ''+str(self.uin_user)+'  '+str(self.fio_user)



    

class Results_sport_competition(models.Model):
    id_user = models.ForeignKey(Student, on_delete=models.CASCADE)
    id_sport_competition = models.ForeignKey(Sport_competition, on_delete=models.CASCADE)
    results_sport_competition = models.CharField(max_length=10)
    date = models.DateField()
    number_of_try = models.PositiveIntegerField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return ''+str(self.id_user)+'  '+str(self.id_sport_competition)+'  '+str(self.results_sport_competition)

class Norm_gto(models.Model):
    TYPES_OF_NORM = [
        ('Gold', 'Золото'),
        ('Silver', 'Серебро'),
        ('Bronze', 'Бронза')
    ]
    
    id_sport_competition = models.ForeignKey(Sport_competition, on_delete=models.CASCADE)
    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField()
    gender = models.SmallIntegerField(choices = Student.GENDERS)
    type_of_norm = models.CharField(max_length=10, choices=TYPES_OF_NORM)
    boundary_first = models.DecimalField(max_digits=4,decimal_places=2)
    boundary_second = models.DecimalField(max_digits=4,decimal_places=2)
