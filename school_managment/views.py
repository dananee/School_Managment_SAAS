from base64 import urlsafe_b64decode
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from school_managment.permissions import IsStaffOrAdminUser
from .serialization import CustomPasswordResetConfirmSerializer, CustomTokenObtainPairSerializer,   PersonSerializer, ScheduleClassSerializer, SchoolDataSerializer, ClassSerializer, SchoolMembersSerializer, TeacherSerializer, SubjectSerializer, ClassRoomSerializer
from .models import ClassSchedule, Person, SchoolDataModel, Class, SchoolMembers, Teacher, Subject, ClassRoom
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from djoser import views as djoser_views
from django.utils.http import base36_to_int
from djoser.serializers import PasswordResetConfirmSerializer
# from djoser.views import PasswordResetConfirmView as DjoserPasswordResetConfirmView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


class SchoolDataView(viewsets.ModelViewSet):

    queryset = SchoolDataModel.objects.all()
    serializer_class = SchoolDataSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsStaffOrAdminUser]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer


class PersonViewSet(viewsets.ViewSet):

    permission_classes_by_action = {
        "default": [IsAuthenticated],
        "retrieve": [IsAuthenticated, IsAdminUser],
        'list': [IsAdminUser],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser],
        'destroy': [IsAdminUser, ]
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            # action is not set return default permission_classes
            return [
                permission()
                for permission in self.permission_classes_by_action["default"]
            ]

    def list(self, request):

        queryset = Person.objects.all()
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            person = Person.objects.get(pk=pk)
            serializer = PersonSerializer(person)
            return Response(serializer.data)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            person = Person.objects.get(pk=pk)
            serializer = PersonSerializer(person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            person = Person.objects.get(pk=pk)
            person.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SchoolMembersViewSet(viewsets.ModelViewSet):

    permission_classes_by_action = {
        "default": [IsAuthenticated],
        "retrieve": [IsAuthenticated, IsAdminUser],
        'list': [IsAdminUser],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser],
        'destroy': [IsAdminUser, ]
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            # action is not set return default permission_classes
            return [
                permission()
                for permission in self.permission_classes_by_action["default"]
            ]

    queryset = SchoolMembers.objects.all()
    serializer_class = SchoolMembersSerializer

    def list(self, request):
        school_id = request.data.get('school_id')
        queryset = SchoolMembers.objects.filter(school=school_id)

        serializer = SchoolMembersSerializer(queryset, many=True)
        return Response(serializer.data)


class ScheduleClassesViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ScheduleClassSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomPasswordResetConfirmView(viewsets.ViewSet):
    serializer_class = CustomPasswordResetConfirmSerializer

    def create(self, request):
        print("éééééééééééééééééééé")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({"detail": "Password has been reset"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(Person, pk=uid)
    except (ValueError, Http404):
        raise Http404("Invalid user ID")

    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            re_new_password = request.POST.get('re_new_password')
            if new_password != "":
                # Update the user's password
                user.set_password(new_password)

                user.save()
                # Redirect to a success page or display a success message
                return render(request, 'password_reset_success.html')
            else:
                print(f"Error {new_password} - {re_new_password}")
                # Passwords do not match, render the password reset form with an error
                return render(request, 'password_reset.html', {'uidb64': uidb64, 'token': token, 'error_message': "Passwords do not match"})
        else:
            return render(request, 'password_reset.html', {'uidb64': uidb64, 'token': token})
    else:
        raise Http404("Invalid password reset link.")


def activation_email_account(request, uidb64, token):
    print(f"*********  - {uidb64} ************")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(Person, pk=uid)
    except (ValueError, Http404):
        raise Http404("Invalid user ID")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Redirect to a success page or display a success message
        return render(request, 'confirmation.html')

    else:
        raise Http404("Invalid password reset link.")
