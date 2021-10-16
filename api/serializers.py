from django.db import models
from django.db.models import fields
from rest_framework import serializers
from application.models import *
from django.contrib.auth.models import User


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        # exclude = ['university']

