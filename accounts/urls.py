from django.urls import  path
from .views import LoginView, TestApi

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("test/", TestApi.as_view(), name="test"),
]
 
