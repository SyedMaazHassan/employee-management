from django.db import models
from django.db.models import fields
from rest_framework import serializers
from application.models import *
from django.contrib.auth.models import User


class EmployeeSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Employee
        fields = "__all__"
        # exclude = ['university']

    def validate(self, data):
        errors = {}
        if 'phone' in data:
            phone = data['phone']
            if not phone.replace(" ", "").isdigit():
                errors['Phone'] = "Phone number can't contain alphabets"

        if 'telephone' in data:
            telephone = data['telephone']
            if not telephone.replace(" ", "").isdigit():
                errors['Telephone'] = "Telephone number can't contain alphabets"

        if 'birthday' in data:
            if data['birthday'].year > 2002:
                errors['Age'] = "Employee age can't be less than 18 years"

        if 'company' in data and data['company']:
            company = data['company']
            email = data['email']
            phone = data['phone']
            telephone = data['telephone']
            query = Employee.objects.filter(
                email=email,  company=company) | Employee.objects.filter(phone=phone, company=company) | Employee.objects.filter(telephone=telephone, company=company)
            if query.count() != 0:
                errors['unique_constraint'] = "Employee with given email, phone or telephon already exists in this company!"

        if len(errors.keys()) > 0:
            raise serializers.ValidationError(errors)

        return data


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        # fields = "__all__"
        exclude = ['company_admin', 'id']

    def validate(self, data):
        errors = {}
        if 'phone' in data:
            phone = data['phone']
            if not phone.replace(" ", "").isdigit():
                errors['Phone'] = "Phone number can't contain alphabets"

        if 'telephone' in data:
            telephone = data['telephone']
            if not telephone.replace(" ", "").isdigit():
                errors['Telephone'] = "Telephone number can't contain alphabets"

        if 'birthday' in data:
            if data['birthday'].year > 2002:
                errors['Age'] = "Employee age can't be less than 18 years"

        if 'company' in data and data['company']:
            company = data['company']
            email = data['email']
            phone = data['phone']
            telephone = data['telephone']
            query = Employee.objects.filter(
                email=email,  company=company) | Employee.objects.filter(phone=phone, company=company) | Employee.objects.filter(telephone=telephone, company=company)
            if query.count() != 0:
                errors['unique_constraint'] = "Employee with given email, phone or telephon already exists in this company!"

        if len(errors.keys()) > 0:
            raise serializers.ValidationError(errors)

        return data
