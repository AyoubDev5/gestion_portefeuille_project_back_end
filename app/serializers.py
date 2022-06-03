from rest_framework import serializers
from .models import User, Department, Employee, Tache, Project, Material


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #what you most enter
        fields = ['id', 'name', 'email', 'password', 'role']
        #don't return the pwd
        extra_kwargs = {  
            'password': {'write_only': True}
        }

    #hashing password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('__all__') 

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('__all__') 

class TacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache
        fields = ('__all__')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        #fields = ('id','name','date_debut','date_fin','description','department','team')
        fields = ('__all__')

class ProjectSerializerCalendar(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title','start_date','end_date')

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('__all__')
