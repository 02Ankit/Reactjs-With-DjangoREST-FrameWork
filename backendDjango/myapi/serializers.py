from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import UsersProf

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersProf
        fields = ['id', 'username', 'email']