from django.urls import path
from . import views
from api.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('get-employees/', EmployeeApi.as_view()),
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
