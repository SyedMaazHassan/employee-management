from django.shortcuts import render
from api.serializers import EmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
# Create your views here.
from application.models import *


def index(request):
    return render(request, "test.html")


class EmployeeApi(APIView):
    def get(self, request):
        output = {}
        # Getting students
        all_employees = Employee.objects.all()
        # Serializing -> converting to JSON
        serializer = EmployeeSerializer(all_employees, many=True)
        output['status'] = 200
        output['payload'] = serializer.data
        return Response(output)

    def post(self, request):
        output = {}
        data = request.data

        # Creating record
        serializer = EmployeeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            output['status'] = 200
            output['message'] = "Student is saved successfully!"
            output['details'] = serializer.data
        else:
            output['status'] = 403
            output['message'] = "Something went wrong!"
            output['errors'] = serializer.errors

        return Response(output)

    def update_details(self, request, partial=False):
        output = {
            'status': 403,
            'message': "Request failed"
        }
        try:
            id = request.data['id']
            student = Student.objects.get(id=id)
            if partial:
                serializer = EmployeeSerializer(
                    instance=student, data=request.data, partial=True)
            else:
                serializer = EmployeeSerializer(
                    instance=student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                output['status'] = 200
                output['message'] = "Student record updated successfully!"
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

    def delete(self, request):
        output = {}
        try:
            id = request.data['id']
            student = Student.objects.get(id=id)
            serializer = EmployeeSerializer(instance=student, many=False)
            student.delete()
            output['status'] = 200
            output['message'] = "Student has been deleted!"
            output['details'] = serializer.data
        except Exception as e:
            output['status'] = 200
            output['message'] = "Request failed!"
            output['details'] = str(e)

        return Response(output)
