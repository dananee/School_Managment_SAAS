from base64 import urlsafe_b64decode
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from school_managment.permissions import IsStaffOrAdminUser, IsTeacherOrAdminUser
from .serialization import (
    AttendanceChartSerializers,
    AttendanceSerializer,
    CustomPasswordResetConfirmSerializer,
    CustomTokenObtainPairSerializer,
    EventsSerializer,
    ExamSerializers,
    NotificationSerializer,
    ParentSerializer,
    PerformanceSerializer,
    PersonSerializer,
    ResultSerializers,
    ScheduleClassSerializer,
    SchoolDataSerializer,
    ClassSerializer,
    SchoolMembersSerializer,
    StaffSerialization,
    StudentSerializer,
    TeacherSerializer,
    SubjectSerializer,
    ClassRoomSerializer,
)
from .models import (
    Attendance,
    ClassSchedule,
    Events,
    Exam,
    Notification,
    Parent,
    Person,
    Result,
    SchoolDataModel,
    Classe,
    SchoolMembers,
    Staff,
    Student,
    Teacher,
    Subject,
    ClassRoom,
)
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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime
channel_layer = get_channel_layer()


def send_notification_by_role(role, message, data):
    print(f"ROLE {role} {data}")
    users_with_role = SchoolMembers.objects.filter(role=role)
    for school_member in users_with_role:
         
        notification_serializer = NotificationSerializer(data=data)

        if notification_serializer.is_valid():

            notification_serializer.save()
        now = datetime.datetime.now()
        async_to_sync(channel_layer.group_send)(
            f"role_{role}",
            {
                "type": "send_notification",
                "message": message,
                "timestamp": now ,  # Convert timestamp to ISO format
            },
        )


class SchoolDataView(viewsets.ModelViewSet):

    queryset = SchoolDataModel.objects.all()
    serializer_class = SchoolDataSerializer


class ClassViewSet(viewsets.ModelViewSet):

    http_method_names = ["patch", "get", "post", "delete", "put"]
    permission_classes_by_action = {
        "default": [IsAuthenticated],
        "retrieve": [IsAuthenticated, IsAdminUser],
        "list": [IsAdminUser],
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [
            IsAdminUser,
        ],
    }
    queryset = Classe.objects.all()
    serializer_class = ClassSerializer

    def list(self, request):
        school_id = request.data.get("school_id")
        queryset = Classe.objects.filter(school=school_id)

        serializer = ClassSerializer(queryset, many=True)
        return Response(serializer.data)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsStaffOrAdminUser]

    def list(self, request):
        school_id = request.data.get("school_id")
        queryset = Teacher.objects.filter(user__school=school_id)

        serializer = TeacherSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            queryset = Teacher.objects.get(user__id=pk)

            serializer = TeacherSerializer(queryset)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            instance = Teacher.objects.get(pk=pk)
            serializer = TeacherSerializer(instance, data=request.data, partial=True)
            print(f"Teacher {pk} -  ")
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):

        try:
            teacher = Teacher.objects.get(pk=pk)
            serializer = TeacherSerializer(teacher, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class StudentViewSet(viewsets.ModelViewSet):

    permission_classes_by_action = {
        "default": [IsAdminUser],
        "retrieve": [IsTeacherOrAdminUser],
        "list": [IsStaffOrAdminUser],
        "create": [IsStaffOrAdminUser],
        "update": [IsStaffOrAdminUser],
        "partial_update": [IsStaffOrAdminUser],
        "destroy": [
            IsStaffOrAdminUser,
        ],
    }
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

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
        school_id = request.query_params.get("school_id")
        
        queryset = Student.objects.filter(user__school=school_id)

        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsStaffOrAdminUser]

    def list(self, request):
        school_id = request.data.get("school_id")
        queryset = Parent.objects.filter(user__school=school_id)

        serializer = ParentSerializer(queryset, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrAdminUser]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

    def retrieve(self, request, pk=None):
        try:
            queryset = ClassRoom.objects.filter(assigned_teacher__user__id=pk)

            serializer = ClassRoomSerializer(queryset, many=True)
            return Response(serializer.data)
        except ClassRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PersonViewSet(viewsets.ViewSet):
    http_method_names = ["patch", "get", "post", "delete", "put"]
    permission_classes_by_action = {
        "default": [IsAuthenticated],
        "retrieve": [IsAuthenticated, IsAdminUser],
        "list": [IsAdminUser],
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [
            IsAdminUser,
        ],
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

    def partial_update(self, request, pk=None):
        try:
            instance = Person.objects.get(pk=pk)
            serializer = PersonSerializer(instance, data=request.data, partial=True)
            print(f"Person {pk} - {instance.email} - {request.data}")
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
    http_method_names = ["patch", "get", "post", "delete", "put"]
    permission_classes_by_action = {
        "default": [IsAuthenticated],
        "retrieve": [IsAuthenticated, IsAdminUser],
        "list": [IsAdminUser],
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [
            IsAdminUser,
        ],
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
        school_id = request.data.get("school_id")
        queryset = SchoolMembers.objects.filter(school=school_id)

        serializer = SchoolMembersSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            instance = SchoolMembers.objects.get(pk=pk)
            serializer = SchoolMembersSerializer(
                instance, data=request.data, partial=True
            )
            print(f"MEMEBER {pk} - {instance.person.email} - ")
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ScheduleClassesViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ScheduleClassSerializer

    def list(self, request):
        school_id = request.data.get("school_id")
        queryset = self.queryset.model.objects.filter(
            class_room__assigned_teacher__user__school=school_id
        )

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomPasswordResetConfirmView(viewsets.ViewSet):
    serializer_class = CustomPasswordResetConfirmSerializer

    def create(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {"detail": "Password has been reset"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(Person, pk=uid)
    except (ValueError, Http404):
        raise Http404("Invalid user ID")

    if default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("new_password")
            re_new_password = request.POST.get("re_new_password")
            if new_password != "":
                # Update the user's password
                user.set_password(new_password)

                user.save()
                # Redirect to a success page or display a success message
                return render(request, "password_reset_success.html")
            else:
                print(f"Error {new_password} - {re_new_password}")
                # Passwords do not match, render the password reset form with an error
                return render(
                    request,
                    "password_reset.html",
                    {
                        "uidb64": uidb64,
                        "token": token,
                        "error_message": "Passwords do not match",
                    },
                )
        else:
            return render(
                request, "password_reset.html", {"uidb64": uidb64, "token": token}
            )
    else:
        raise Http404("Invalid password reset link.")


def activation_email_account(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(Person, pk=uid)
    except (ValueError, Http404):
        raise Http404("Invalid user ID")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Redirect to a success page or display a success message
        return render(request, "confirmation.html")

    else:
        raise Http404("Invalid password reset link.")


class LogoutAndBlacklistRefreshTokenForUserView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            print(f"Refresh ======> {refresh_token}")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveAPIView):
    queryset = SchoolMembers.objects.all()
    serializer_class = SchoolMembersSerializer

    def retrieve(self, request, pk=None):

        queryset = SchoolMembers.objects.filter(person=request.user)

        serializer = SchoolMembersSerializer(queryset, many=True)
        if request.user and pk == "me":
            return Response(SchoolMembersSerializer(request.user).data)
        return Response(serializer.data[0])


class EventsView(viewsets.ModelViewSet):

    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    def list(self, request):
        school_id = request.data.get("school_id")
        queryset = self.queryset.model.objects.filter(school=school_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class AttendanceView(viewsets.ModelViewSet):

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def list(self, request):
        school_id = request.data.get("school_id")
        queryset = self.queryset.model.objects.filter(school=school_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class NotificationView(viewsets.ModelViewSet):
    
    queryset = Notification.objects.order_by("-timestamp")
    serializer_class = NotificationSerializer

    def list(self, request):
        school_id = request.data.get("school_id")
        queryset = self.queryset.model.objects.filter(sender__school=school_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        queryset = self.queryset.model.objects.filter(role=pk).order_by(
            "-timestamp"
        )

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

     


class ResultView(viewsets.ModelViewSet):

    queryset = Result.objects.all()
    serializer_class = ResultSerializers

    def list(self, request):
        school_id = request.data.get("school_id")
        queryset = self.queryset.model.objects.filter(student__user__school=school_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class StaffView(viewsets.ModelViewSet):

    queryset = Staff.objects.all()
    serializer_class = StaffSerialization
    permission_classes = [IsStaffOrAdminUser]

    def list(self, request):
        school_id = request.data.get("school_id")
        queryset = self.queryset.model.objects.filter(user__school=school_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StaffSerialization(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentPerformanceViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = PerformanceSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializers
    permission_classes = [IsStaffOrAdminUser]

    def list(self, request):
        school_id = request.query_params.get("school_id")
        queryset = Exam.objects.filter(school=school_id)
        serializer = ExamSerializers(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request,pk=None):
        school_id = request.query_params.get("school_id")
        teacher_id = request.query_params.get("teacher_id")
        queryset = Exam.objects.filter(school=school_id,teacher__user__id=teacher_id)
        serializer = ExamSerializers(queryset, many=True)
        return Response(serializer.data)