from django.urls import path, re_path
from .views import RegisterView, LoginView, UserView,LogoutView,DepartmentDetails,EmployeeDetails,TacheDetails,ProjectDetails,MaterialDetails
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('dep/<int:pk>/', DepartmentDetails.as_view()),
    path('empl/<int:pk>/', EmployeeDetails.as_view()),
    path('tach/<int:pk>/', TacheDetails.as_view()),
    path('proj/<int:pk>/', ProjectDetails.as_view()),
    path('mater/<int:pk>/', MaterialDetails.as_view()),

    re_path(r'^departments$',views.DepartmentApi),
    re_path(r'^department/([0-9]+)$',views.DepartmentApi),    

    re_path(r'^employees$',views.EmployeeApi),
    re_path(r'^employee/([0-9]+)$',views.EmployeeApi),

    re_path(r'^taches$',views.TacheApi),
    re_path(r'^tache/([0-9]+)$',views.TacheApi),

    re_path(r'^projects$',views.ProjectApi),
    re_path(r'^project/([0-9]+)$',views.ProjectApi),

    re_path(r'^materials$',views.MaterialApi),
    re_path(r'^material/([0-9]+)$',views.MaterialApi),

    re_path(r'^depart/([0-9]+)/allProCalendar$',views.ProjectByDepIdCalendar),

    re_path(r'^depart/([0-9]+)/Allproject$',views.ProjectByDepId),
    re_path(r'^projet/([0-9]+)/Allmateriel$',views.MaterielByProjId),
    # re_path(r'^projet/([0-9]+)/team/([0-9]+)/Allemploy$',views.EmployByTeamId_TeamByProjId),
    # re_path(r'^projet/([0-9]+)/team/([0-9]+)/employ/([0-9]+)/tache$',views.TacheByEmployId_EmployByTeamId_TeamByProjId),
    
    re_path(r'^projet/([0-9]+)/materialCount$',views.materialCount),
    re_path(r'^projet/([0-9]+)/employCount$',views.employCount),
    re_path(r'^projet/([0-9]+)/tacheCount$',views.tacheCount),

    re_path(r'^projet/([0-9]+)/tacheisActive$',views.tacheisActive),
    re_path(r'^projet/([0-9]+)/tacheisNotActive$',views.tacheisNotActive),
]