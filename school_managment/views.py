from base64 import urlsafe_b64decode
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from school_managment.permissions import IsStaffOrAdminUser
from .serialization import CustomTokenObtainPairSerializer,   PersonSerializer, ScheduleClassSerializer, SchoolDataSerializer, ClassSerializer, SchoolMembersSerializer, TeacherSerializer, SubjectSerializer, ClassRoomSerializer
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
        if request.user.is_superuser:
            queryset = Person.objects.all()
            serializer = PersonSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

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
    queryset = SchoolMembers.objects.all()
    serializer_class = SchoolMembersSerializer


class ScheduleClassesViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ScheduleClassSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def password_reset_confirm(request, uidb64, token):
    try:
        uid = base36_to_int(uidb64)
        user = get_object_or_404(Person, pk=uidb64)
    except ValueError:
        raise Http404("Invalid user ID")
    except Person.DoesNotExist:
        raise Http404("Person not found")

    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            serializer = djoser_views.PasswordResetConfirmSerializer(data={
                'uid': uidb64,
                'token': token,
                'new_password': new_password
            })
            if serializer.is_valid():
                serializer.save()
                # Redirect to a success page or display a success message
                return redirect('password_reset_success')
            else:
                # Handle invalid serializer data (e.g., new password does not meet requirements)
                # You may render the confirmation page again with error messages
                return render(request, 'password_reset.html', {'uidb64': uidb64, 'token': token, 'errors': serializer.errors})
        else:
            return render(request, 'password_reset.html', {'uidb64': uidb64, 'token': token})
    else:
        raise Http404("Invalid password reset link.")
