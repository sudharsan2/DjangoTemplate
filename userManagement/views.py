from django.shortcuts import render
from .serializer import (
    RegisterSerializer,loginSerializer,UserSerializer)
from rest_framework.response import Response
from rest_framework import generics, status

# Create your views here.
class RegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        userpayload = request.data.copy()
        empId = userpayload['empId']
        dict1 = {
            "empId": userpayload['empId'],
            "name" : userpayload['username']
        }
        roles_data = userpayload.pop('roles', [])
        serializer = self.serializer_class(data=userpayload)
        serializer.is_valid(raise_exception=True)
        user_instance=serializer.save()
        for role_id in roles_data:
            # Add each role to the user instance
            user_instance.roles.add(role_id)

        user_data = serializer.data
        # user_obj = user.objects.get(email=user_data.get('email'))
        # token = RefreshToken.for_user(user_obj).access_token
        # mail=sendMail()
        # content=emailHtmlLoader.userCreatedMail(userpayload)
        # subject='User created'
        # receipient=[]
        # receipient.append(userpayload.get('email', None))
        # mail.sendMailtoReceipients(content, subject, receipient)

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class=loginSerializer
    def post(self, request):
         user = request.data
         serializer = self.serializer_class(data=user)
         serializer.is_valid(raise_exception=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
