from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from pyzbar import pyzbar
from PIL import Image
from django.db.models import Q

# main page function


# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name": name,
            "l_name": l_name,
            "email": email,
            "pass1": pass1,
            "pass2": pass2,
        }
        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email"
                return render(request, "signup.html", context)

            user = User.objects.create_user(
                username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()

            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)

    return render(request, "signup.html")


def get_company_by_admin(user_object):
    company_admin = CompanyAdmin.objects.get(user=user_object)
    company = Company.objects.get(company_admin=company_admin)
    return company
# function for login


# function for logout
def logout(request):
    auth.logout(request)
    return redirect("index")

# function for rendering the dashboard


@login_required
def dashboard(request):
    context = {
        "name": "dashboard"
    }

    return render(request, "index.html", context)


def read_qr(image):
    try:
        qr_code = pyzbar.decode(image)[0]
        # convert into string
        data = qr_code.data.decode("utf-8")
        return data
    except:
        return False


@login_required
def delete_employee(request, id):
    try:
        employee = Employee.objects.get(id=id)
        company = get_company_by_admin(request.user)
        if employee.company == company:
            employee.is_deleted = True
            employee.is_active = False
            employee.save()
            messages.info(request, "Employee has been deleted successfully!")
        else:
            raise ValueError(
                "This employee doesn't belong to your company, you can't delete it!")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("index")


@login_required
def upload_qr_code(request):
    if request.method == "POST":
        qr_code = request.FILES['upload_qr_input']

        # saving into a model to save file in the folder
        new_scan = Scan(my_file=qr_code)
        new_scan.save()

        # getting base path
        BASE_DIR = settings.BASE_DIR
        # Making full path of the file
        file_path = os.path.join(BASE_DIR, "media", str(new_scan.my_file))
        # Calling a function which is using pyzbar
        # to detect and scan qr code
        image = Image.open(file_path)
        qr_content = read_qr(image)

        # printing the value of QR code
        if qr_content and len(qr_content) > 0:
            try:
                scanned_url = qr_content
                # for verification
                employee_id = scanned_url.split("/")[-1]

                query = Employee.objects.filter(id=employee_id)
                if query.exists():
                    employee = query[0]
                    company = get_company_by_admin(request.user)
                    if employee.company == company:

                        new_scan.delete()
                        os.remove(file_path)

                        return redirect(scanned_url)

                        # return redirect(f"/employee/{employee.id}/1")
                    else:
                        messages.error(
                            request, "Since this employee doesn't belong to your company, you can't acccess this profile!")
                else:
                    messages.error(
                        request, "No employee exists with this QR code!")

            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(
                request, "QR code not detected in the image OR picture is very unclear!")

        return redirect("index")

    return redirect("login")


@login_required
def all_employees(request):
    context = {
        "name": "all-employees"
    }

    parameter = False
    if 'deleted' in request.GET and request.GET['deleted']:
        parameter = request.GET['deleted']

    print(parameter)

    search_query = request.GET.get('query')
    company = get_company_by_admin(request.user)

    if not parameter:
        all_employees = Employee.objects.filter(
            company=company, is_deleted=False)
    else:
        all_employees = Employee.objects.filter(
            company=company, is_deleted=True)

    context['company'] = company

    if search_query:
        search_query = search_query.strip()
        filtered_records = Employee.objects.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(
                email__icontains=search_query) | Q(designation__icontains=search_query) | Q(phone__icontains=search_query)
        )
        # all_employees_list = []
        # for employee in all_employees:
        #     if search_query == employee.first_name:
        #         all_employees_list.append(employee)
        #     elif search_query == employee.last_name:
        #         all_employees_list.append(employee)
        #     elif search_query == employee.email:
        #         all_employees_list.append(employee)
        #     elif search_query == employee.designation:
        #         all_employees_list.append(employee)
        #     elif search_query == employee.phone:
        #         all_employees_list.append(employee)

        context['all_employees'] = filtered_records
    else:
        context['all_employees'] = all_employees

    context['all_employees'] = list(context['all_employees'])[::-1]

    return render(request, "all-employees.html", context)


@login_required
def save_employee(request):
    if request.method == "POST":
        profile_picture = None
        is_active = False
        telephone = None
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
        if 'is_active' in request.POST:
            is_active = True
        if 'telephone' in request.POST:
            telephone = request.POST['telephone']

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        designation = request.POST['designation']
        birthday = request.POST['birthday']
        projects = request.POST['projects']
        specialized_in = request.POST['specialized_in']

        # Get current admin
        current_admin = CompanyAdmin.objects.get(user=request.user)
        # Get current company
        company = Company.objects.get(company_admin=current_admin)

        # Check if this user has already been created
        query = Employee.objects.filter(
            email=email,  company=company) | Employee.objects.filter(phone=phone, company=company)

        if query.count() == 0:
            # Creating new employee
            new_employee = Employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                designation=designation,
                phone=phone,
                birthday=birthday,
                company=company,
                is_active=is_active,
                projects=projects,
                specialized_in=specialized_in
            )
            if profile_picture:
                new_employee.profile_picture = profile_picture
            if telephone:
                new_employee.telephone = telephone

            new_employee.save()
            messages.info(request, "New employee has been registered!")
        else:
            messages.error(request, "This employee already exists!")

        return redirect("/all-employees/")

    return redirect("login")


@login_required
def update_employee(request):

    return redirect("login")


def single_employee(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            if id and len(id) > 0:
                employee = Employee.objects.filter(id=id)
                if employee.exists():
                    employee = employee[0]

                    company = get_company_by_admin(request.user)
                    if employee.company == company:

                        if 'profile_picture' in request.FILES and request.FILES['profile_picture']:
                            employee.profile_picture = request.FILES['profile_picture']
                        is_active = False
                        telephone = None
                        is_deleted = True

                        if 'is_active' in request.POST:
                            is_active = True
                            is_deleted = False
                        if 'telephone' in request.POST:
                            employee.telephone = request.POST['telephone']

                        employee.is_active = is_active
                        employee.first_name = request.POST['first_name']
                        employee.last_name = request.POST['last_name']
                        employee.email = request.POST['email']
                        employee.phone = request.POST['phone']
                        employee.designation = request.POST['designation']
                        employee.birthday = request.POST['birthday']
                        employee.projects = request.POST['projects']
                        employee.specialized_in = request.POST['specialized_in']
                        employee.is_deleted = is_deleted
                        employee.save()

                        messages.info(
                            request, "Employee info has been updated successfully!")
                    else:
                        messages.error(
                            request, "This employee doesn't belong to your company!")
                else:
                    messages.error(request, "No employee exists with this id!")
            else:
                messages.error(request, "Invalid id!")

            return redirect(f"/employee/{id}")

    context = {
        "employee": None,
        "index": 1
    }
    employee = Employee.objects.filter(id=id)

    if employee.exists():
        employee = employee[0]
        context['employee'] = employee

    if request.user.is_authenticated:
        return render(request, "profile.html", context)
    else:
        return render(request, "temp-profile.html", context)


@login_required
def edit_company_details(request):
    company = get_company_by_admin(request.user)
    if request.method == "POST":
        try:
            name = request.POST['name']
            tagline = request.POST['tagline']
            description = request.POST['description']
            founded_in = request.POST['founded_in']
            error_message = "Kindly provide valid values for all fields!"
            if name:
                company.name = name
            else:
                raise ValueError(error_message)
            if tagline:
                company.tagline = tagline
            else:
                raise ValueError(error_message)
            if description:
                company.description = description
            else:
                raise ValueError(error_message)
            if founded_in:
                company.founded_in = founded_in
            else:
                raise ValueError(error_message)

            if 'template_input' in request.POST and request.POST['template_input']:
                template_id = request.POST['template_input']
                template_query = CardTemplate.objects.filter(id=template_id)
                if template_query.exists():
                    template = template_query[0]
                    company.card_template = template

            company.save()
            messages.info(
                request, "Company information has been updated successfully!")
        except Exception as e:
            messages.error(request, "Provide the valid information!")

        return redirect("edit-company-details")

    context = {
        "name": "edit-company-details"
    }
    context['card_templates'] = CardTemplate.objects.all()
    context['company'] = company
    return render(request, "edit-company-details.html", context)


def buttons(request):
    return render(request, "buttons.html")


def dropdowns(request):
    return render(request, "dropdowns.html")


def typography(request):
    return render(request, "typography.html")


def basic_elements(request):
    return render(request, "basic_elements.html")


def chartjs(request):
    return render(request, "chartjs.html")


def basictable(request):
    return render(request, "basic-table.html")


def icons(request):
    return render(request, "mdi.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)

            redirection = request.POST['redirection']
            if redirection and len(redirection) > 0:
                return redirect(redirection)
            else:
                return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def error_404(request):
    return render(request, "error-404.html")


def error_500(request):
    return render(request, "error-500.html")


def documentation(request):
    return render(request, "documentation.html")


def profile(request):
    return render(request, "profile.html")
