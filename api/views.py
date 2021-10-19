from django.shortcuts import render
from api.serializers import CompanySerializer, EmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
# Create your views here.
from application.models import *


def index(request):
    return render(request, "test.html")


class GetEmployeeApi(APIView):
    def get(self, request):
        output = {}
        is_deleted = request.data['is_deleted']
        if is_deleted and is_deleted == "true":
            all_employees = Employee.objects.filter(
                is_deleted=True, is_active=False)
        else:
            all_employees = Employee.objects.filter(
                is_deleted=False, is_active=True)

        # Getting students
        # Serializing -> converting to JSON
        serializer = EmployeeSerializer(all_employees, many=True)
        output['status'] = 200
        output['payload'] = serializer.data
        return Response(output)


class SaveEmployeeApi(APIView):
    def post(self, request):
        output = {}
        data = request.data

        # Creating record
        serializer = EmployeeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            output['status'] = 200
            output['message'] = "Employee is saved successfully!"
            output['details'] = serializer.data
        else:
            output['status'] = 403
            output['message'] = "Something went wrong!"
            output['errors'] = serializer.errors

        return Response(output)


class UpdateEmployeeApi(APIView):
    def update_details(self, request, partial=False):
        output = {
            'status': 403,
            'message': "Request failed"
        }
        try:
            id = request.data['id']
            print(id)
            student = Employee.objects.get(id=id)
            if partial:
                serializer = EmployeeSerializer(
                    instance=student, data=request.data, partial=True)
            else:
                serializer = EmployeeSerializer(
                    instance=student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                output['status'] = 200
                output['message'] = "Employee record updated successfully!"
                output['details'] = serializer.data
            else:
                output['errors'] = serializer.errors
        except Exception as e:
            output['errors'] = str(e)

        return output

    def patch(self, request):
        output = self.update_details(request, True)
        return Response(output)

    def put(self, request):
        output = self.update_details(request, False)
        return Response(output)


class DeleteEmployeeApi(APIView):
    def delete(self, request):
        output = {}
        print(request.data['id'])
        try:
            id = request.data['id']
            employee = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(instance=employee, many=False)
            employee.is_active = False
            employee.is_deleted = True
            employee.save()
            output['status'] = 200
            output['message'] = "Employee has been deleted!"
            output['details'] = serializer.data
        except Exception as e:
            output['status'] = 200
            output['message'] = "Request failed!"
            output['details'] = str(e)

        return Response(output)


class UndeleteEmployeeApi(APIView):
    def post(self, request):
        output = {}
        id = request.data['id']
        try:
            id = request.data['id']
            employee = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(instance=employee, many=False)
            employee.is_active = True
            employee.is_deleted = False
            employee.save()
            output['status'] = 200
            output['message'] = "Employee has been undeleted and active now!"
            output['details'] = serializer.data
        except Exception as e:
            output['status'] = 200
            output['message'] = "Request failed!"
            output['details'] = str(e)

        return Response(output)


class GetCompanyApi(APIView):
    def get(self, request):
        output = {}
        if 'id' in request.data:
            id = request.data['id']
            company = get_object_or_404(Company, id=id)
            print(company)
            # Serializing -> converting to JSON
            serializer = CompanySerializer(company, many=False)
            output['status'] = 200
            output['payload'] = serializer.data
        else:
            output['status'] = 403
            output['message'] = "Company ID is required!"

        return Response(output)


class UpdateCompanyApi(APIView):
    def update_details(self, request, partial=False):
        output = {
            'status': 403,
            'message': "Request failed"
        }
        try:
            id = request.data['id']
            student = Company.objects.get(id=id)
            if partial:
                serializer = CompanySerializer(
                    instance=student, data=request.data, partial=True)
            else:
                serializer = CompanySerializer(
                    instance=student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                output['status'] = 200
                output['message'] = "Company record updated successfully!"
                output['details'] = serializer.data
            else:
                output['errors'] = serializer.errors
        except Exception as e:
            output['errors'] = str(e)

        return output

    def patch(self, request):
        output = self.update_details(request, True)
        return Response(output)

    def put(self, request):
        output = self.update_details(request, False)
        return Response(output)
