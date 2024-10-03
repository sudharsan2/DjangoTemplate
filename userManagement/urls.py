from django.urls import path
from .views import (RegistrationView,LoginView)

urlpatterns = [

    path('registration', RegistrationView.as_view()),
    path('signin', LoginView.as_view()),
]
