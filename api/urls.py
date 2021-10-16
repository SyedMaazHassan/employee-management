from django.urls import path
from . import views
from api.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('get-employees/', GetEmployeeApi.as_view()),
    path('save-employee/', SaveEmployeeApi.as_view()),
    path('update-employee/', UpdateEmployeeApi.as_view()),
    path('delete-employee/', DeleteEmployeeApi.as_view()),
    path('undelete-employee/', UndeleteEmployeeApi.as_view()),
    path('get-company-info/', GetCompanyApi.as_view()),
    path('update-company-info/', UpdateCompanyApi.as_view()),
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
