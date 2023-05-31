from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name = 'main'),
    path('profile/', views.profile, name = 'profile'),
    path('enterResults/', views.enterResults, name = 'enterResults'),
    path('main/', views.main, name = 'main'),
    path('history/', views.history, name = 'history'),
    path('standards/', views.standards, name = 'standards'),
    path('contacts/', views.contacts, name = 'contacts'),
    path('studentsPersonal/', views.studentsPersonal, name = 'StudentsPersonal'),
    path('standardsPersonal/', views.standardsPersonal, name = 'standardsPersonal'),
    path('viewResults/', views.ResultsListView.as_view(), name = 'viewResults'),
    path('registration/', views.registration, name = 'registration'),
    path('checkPermission/', views.checkPermission, name = 'checkPermission'),
    path('teacherPersonal/', views.teacherPersonal, name = 'teacherPersonal'),
    path('standardsPersonalTeacher/', views.standardsPersonalTeacher, name = 'standardsPersonalTeacher'),
    path('profileTeacher/', views.profileTeacher, name = 'profileTeacher'),
    path('protocol/', views.protocol, name = 'protocol'),
    path('summaryProtocol/', views.summaryProtocol, name = 'summaryProtocol'),
    path('individualWinner/', views.winner_individual, name='winner_individual'),
    path('teamWinner/', views.winner_team, name='winner_team'),
    path('orgEnterResults/', views.orgEnterResults, name='orgEnterResults'), 
    
]

