from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name="index"),
    path('all-employees/', views.all_employees, name="all-employees"),
    path('employee/<id>', views.single_employee, name="employee"),
    path('delete-employee/<id>', views.delete_employee, name="delete-employee"),
    path('edit-company-details/', views.edit_company_details,
         name="edit-company-details"),
    path('signup', views.signup, name="signup"),
    path('upload-qr-code', views.upload_qr_code, name="upload-qr-code"),
    path('save-employee', views.save_employee, name="save-employee"),
    # path('login', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('buttons/', views.buttons, name="buttons"),
    path('dropdowns/', views.dropdowns, name="dropdowns"),
    path('typography/', views.typography, name="typography"),
    path('basic_elements/', views.basic_elements, name="basic_elements"),
    path('chartjs/', views.chartjs, name="chartjs"),
    path('basictable/', views.basictable, name="basictable"),
    path('icons/', views.icons, name="icons"),
    path('login/', views.login, name="login"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name="profile"),
    path('error_404', views.error_404, name="error_404"),
    path('error_500', views.error_500, name="error_500"),
    path('documentation', views.documentation, name="documentation")

]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
