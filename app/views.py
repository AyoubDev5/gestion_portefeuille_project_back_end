from dataclasses import field
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ProjectSerializerCalendar,UserSerializer, DepartmentSerializer, EmployeeSerializer, TacheSerializer, ProjectSerializer, MaterialSerializer
from .models import User, Department, Employee, Tache, Project, Material
import jwt, datetime
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.db import connection
from django.db.models import Sum, Count,aggregates,F,Value
from django.db.models.functions import Coalesce



# Create your views here.
def index(request):
    return render(request, 'index.html', context=None)
#regiter API (post)
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

#Login API (post)
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        success = True
        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'id': user.id, #store the user id
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), #set how this token will existe (1h)
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        #our cookie its will be send just to the back-end
        response.set_cookie(key='jwt', value=token)
        response.data = {
            'jwt': token,
            'success': success,
            'message': 'Successfully logged in'
        }
        return response

#User API (get) from the cookie return the last user login
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

#Logout API (post)rmove and delete the cookie
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

##############################################################

#Departmenet's CRUD 
@csrf_exempt
def DepartmentApi(request,id=0):
    if request.method=='GET':
        departments = Department.objects.all()
        departments_serializer = DepartmentSerializer(departments, many=True)
        return JsonResponse(departments_serializer.data, safe=False)

    elif request.method=='POST':
        department_data=JSONParser().parse(request)
        departments_serializer = DepartmentSerializer(data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)

    elif request.method=='PUT':
        department_data = JSONParser().parse(request)
        department=Department.objects.get(id=id)
        department_serializer=DepartmentSerializer(department,data=department_data)
        if department_serializer.is_valid():
            department_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        department=Department.objects.get(id=id)
        department.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)

##############################################################
##############################################################

#Employee's CRUD 
@csrf_exempt
def EmployeeApi(request,id=0):
    if request.method=='GET':
        employee = Employee.objects.all()
        employee_serializer = EmployeeSerializer(employee, many=True)
        return JsonResponse(employee_serializer.data, safe=False)

    elif request.method=='POST':
        employee_data=JSONParser().parse(request)
        employees_serializer = EmployeeSerializer(data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)

    elif request.method=='PUT':
        employee_data = JSONParser().parse(request)
        employee=Employee.objects.get(id=id)
        employee_serializer=EmployeeSerializer(employee,data=employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        employee=Employee.objects.get(id=id)
        employee.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)

##############################################################

#Tache's CRUD 
@csrf_exempt
def TacheApi(request,id=0):
    if request.method=='GET':
        tache = Tache.objects.all()
        tache_serializer = TacheSerializer(tache, many=True)
        return JsonResponse(tache_serializer.data, safe=False)

    elif request.method=='POST':
        tache_data=JSONParser().parse(request)
        taches_serializer = TacheSerializer(data=tache_data)
        if taches_serializer.is_valid():
            taches_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)

    elif request.method=='PUT':
        tache_data = JSONParser().parse(request)
        tache=Tache.objects.get(id=id)
        tache_serializer=TacheSerializer(tache,data=tache_data)
        if tache_serializer.is_valid():
            tache_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        tache=Tache.objects.get(id=id)
        tache.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)

##############################################################

#Tache's CRUD 
@csrf_exempt
def ProjectApi(request,id=0):
    if request.method=='GET':
        project = Project.objects.all()
        project_serializer = ProjectSerializer(project, many=True)
        return JsonResponse(project_serializer.data, safe=False)

    elif request.method=='POST':
        project_data=JSONParser().parse(request)
        projects_serializer = ProjectSerializer(data=project_data)
        if projects_serializer.is_valid():
            projects_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)

    elif request.method=='PUT':
        project_data = JSONParser().parse(request)
        project=Project.objects.get(id=id)
        project_serializer=ProjectSerializer(project,data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        project=Project.objects.get(id=id)
        project.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)

##############################################################

#Material's CRUD 
@csrf_exempt
def MaterialApi(request,id=0):
    if request.method=='GET':
        material = Material.objects.all()
        material_serializer = MaterialSerializer(material, many=True)
        return JsonResponse(material_serializer.data, safe=False)

    elif request.method=='POST':
        material_data=JSONParser().parse(request)
        materials_serializer = MaterialSerializer(data=material_data)
        if materials_serializer.is_valid():
            materials_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)

    elif request.method=='PUT':
        material_data = JSONParser().parse(request)
        material=Material.objects.get(id=id)
        material_serializer=MaterialSerializer(material,data=material_data)
        if material_serializer.is_valid():
            material_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        material=Material.objects.get(id=id)
        material.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)

#Get By Id
class DepartmentDetails(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class EmployeeDetails(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class TacheDetails(RetrieveUpdateDestroyAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer

class ProjectDetails(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class MaterialDetails(RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

#other API's

def ProjectByDepId(request,id=0):

   if request.method == 'GET':
        projets = Project.objects.raw(
           "select pro.* "+
           "from app_department as dep,app_project as pro "+
           "where pro.department_id=dep.id and pro.department_id="+id
        )
        project_serializer = ProjectSerializer(projets, many=True)
        return JsonResponse(project_serializer.data, safe=False)

def ProjectByDepIdCalendar(request,id=0):
   if request.method == 'GET':
        projets = Project.objects.filter(department=id).only('id', 'title', 'start_date', 'end_date')
        project_serializer = ProjectSerializerCalendar(projets, many=True)
        return JsonResponse(project_serializer.data, safe=False)

def MaterielByProjId(request,id=0):

     if request.method == 'GET':
        materiels = Material.objects.raw(
           "select * "+
           "from app_material as mat,app_project as pro "+
           "where pro.id=mat.project_id and mat.project_id="+id
        )
        materials_serializer = MaterialSerializer(materiels, many=True)
        return JsonResponse(materials_serializer.data, safe=False)

#get taches by project
def TacheByProjId(request,id=0):

     if request.method == 'GET':
        taches = Tache.objects.raw(
           "select * "+
           "from app_tache as t,app_project as pro "+
           "where pro.id=t.project_id and t.project_id="+id
        )
        taches_serializer = TacheSerializer(taches, many=True)
        return JsonResponse(taches_serializer.data, safe=False)

def EmployByTeamId_TeamByProjId(request,idPro=0):

     if request.method == 'GET':
        empl = Employee.objects.raw(
            "select emp.* "+
            "from app_employee as emp ,app_project as pro, app_tache as tache "+
            "where tache.employee_id=emp.id and pro.id=tache.project_id and pro.id="+idPro
        )
        empl_serializer = EmployeeSerializer(empl, many=True)
        return JsonResponse(empl_serializer.data, safe=False)  

# def TacheByEmployId_EmployByTeamId_TeamByProjId(request,idPro=0,idTeam=0,idEmpl=0):

#      if request.method == 'GET':
#         tache = Tache.objects.raw(
#             "select tache.* "+
#             "from app_tache as tache, app_employee as emp, app_team as team,app_project as pro "+
#             "where pro.team_id=team.id and emp.team_id=team.id and tache.employee_id=emp.id and "+
#             "emp.id="+idEmpl+" and team.id="+idTeam+" and pro.id="+idPro
#         )
#         tache_serializer = TacheSerializer(tache, many=True)
#         return JsonResponse(tache_serializer.data, safe=False)       

###############
#cards api
def materialCount(request,idPro=0):

     if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute(
            "select  mat.id,Sum( mat.prix* mat.quantity ) as total "+
             "from app_material as mat, app_project as pro "+
             "where mat.project_id = pro.id and pro.id ="+idPro
        )
        total=cursor.fetchone()[1]
        return JsonResponse(total, safe=False)

def employCount(request,idPro=0):

     if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute(
            "select  Count(emp.id) as total "+
            "from app_employee as emp, app_project as pro ,app_team as team "+
            "where team.id = pro.team_id and emp.team_id=team.id and pro.id ="+idPro
        )
        total=cursor.fetchone()[0]
        return JsonResponse(total, safe=False)

def tacheCount(request,idPro=0):

     if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute(
            "select  Count(tache.id) as total "+
            "from app_employee as emp, app_project as pro ,app_team as team, app_tache as tache "+
            "where team.id = pro.team_id and emp.team_id=team.id and tache.employee_id=emp.id and  pro.id ="+idPro
        )
        total=cursor.fetchone()[0]
        return JsonResponse(total, safe=False)

#api chart 
def tacheisActive(request,idPro=0):

     if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute(
            "select  Count(tache.id) as total "+
            "from app_employee as emp, app_project as pro ,app_team as team, app_tache as tache "+
            "where team.id = pro.team_id and emp.team_id=team.id and tache.employee_id=emp.id and tache.isActive=1 and pro.id ="+idPro
        )
        total=cursor.fetchone()[0]
        return JsonResponse(total, safe=False)

def tacheisNotActive(request,idPro=0):

     if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute(
            "select  Count(tache.id) as total "+
            "from app_employee as emp, app_project as pro ,app_team as team, app_tache as tache "+
            "where team.id = pro.team_id and emp.team_id=team.id and tache.employee_id=emp.id and tache.isActive=0 and pro.id ="+idPro
        )
        total=cursor.fetchone()[0]
        return JsonResponse(total, safe=False)


##get user by departmenet ID 
def UserByDepId(request,id=0):

     if request.method == 'GET':
        user = User.objects.raw(
           "select * "+
           "from app_user as user,app_department as dep "+
           "where dep.id=user.department_id and user.department_id="+id
        )
        user_serializer = UserSerializer(user, many=True)
        return JsonResponse(user_serializer.data, safe=False)
