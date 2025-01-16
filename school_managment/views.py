from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.http import Http404,  JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from school_managment.permissions import IsStaffOrAdminUser, IsTeacherOrAdminUser
import requests

from django.shortcuts import get_object_or_404, render

from school_managment.pagination import StandardResultsSetPagination

from .serialization import (

    AttendanceSerializer,
    AttendancesSerializer,
    ClassScheduleSerializer,
    CustomPasswordResetConfirmSerializer,
    CustomTokenObtainPairSerializer,
    EventsSerializer,
    ExamSerializers,
    ExpenseSerializer,
    FCMDeviceSerializer,
    FeeStructureSerializer,
    FinancialReportSerializer,
    MonthlyPaymentSerializer,
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
    StudentLightSerializer,
    StudentSerializer,
    TeacherLightSerializer,
    TeacherSerializer,
    SubjectSerializer,
    ClassRoomSerializer,
    HomeworkSerializer,
    ProfileParentSerializer,
    PubSerializer,
    TransactionSerializer,
    calculate_monthly_performance
)


from .models import (
    Attendance,
    ClassSchedule,
    Events,
    Exam,
    Expense,
    FCMDevice,
    FeeStructure,
    FinancialReport,
    MonthlyPayment,
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
    Homework,
    PubModel,
    Transaction
)
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator

from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend


# from djoser.views import PasswordResetConfirmView as DjoserPasswordResetConfirmView
from django.utils.http import  urlsafe_base64_decode
from django.utils.encoding import  force_str
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.views.generic import TemplateView
from django.db.models import Sum

 
from .NotifManager import send_notification,send_bulk_notifications,send_bulk_class_notifications

class HomePage(TemplateView):
    template_name = "site/index.html"


class MeetingPage(TemplateView):
    template_name = "site/meeting.html"


def calculateAttendSt(schoolId):
    try:
        student = Student.objects.get(user=schoolId)
    except Student.DoesNotExist:
        return {"error": "Student not found"}

    # Get total number of class sessions (or based on a specific schedule, term, etc.)
    total_classes = Attendance.objects.filter(student=student).count()

    # If there's a separate way to calculate total available classes (e.g., from ClassSchedule)
    total_class_sessions = Attendance.objects.filter(
        schedule__isnull=False).count()

    # Calculate the attendance percentage
    attendance_percentage = (
        total_classes / total_class_sessions) * 100 if total_class_sessions > 0 else 0

    # Get the actual attendance details (dates, etc.)
    attended_classes = Attendance.objects.filter(
        student=student).values('date', 'id', 'teacher')

    # Return the data in a dictionary
    return {
        "student_id": schoolId,
        "attendance_percentage": attendance_percentage,
        # List of classes attended by the student
        "attended_classes": list(attended_classes)
    }


 





class SchoolDataView(viewsets.ModelViewSet):
    http_method_names = ["patch", "get", "post", "put"]
    permission_classes_by_action = {
        "default": [IsAdminUser],
        "retrieve": [IsAuthenticated, IsAdminUser],
        "list": [IsAdminUser],
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
    }
    queryset = SchoolDataModel.objects.all()
    serializer_class = SchoolDataSerializer
    pagination_class = StandardResultsSetPagination

    class Meta:
        ordering = ['id']


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

    class Meta:
        ordering = ['id']

    def list(self, request):
        school_id = request.query_params.get("school_id")
        queryset = Classe.objects.filter(school=school_id)

        serializer = ClassSerializer(queryset, many=True)
        return Response(serializer.data)

class TeacherLightViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.order_by('id')
    serializer_class = TeacherLightSerializer
    
    def list(self, request):
        try:
            school_id = request.query_params.get("school_id")
            queryset = Teacher.objects.filter(user__school=school_id)

            serializer = TeacherLightSerializer(queryset, many=True)
            return Response(serializer.data)
        
        except Subject.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class TeacherViewSet(viewsets.ModelViewSet):
    
    queryset = Teacher.objects.order_by('id')
    serializer_class = TeacherSerializer
    permission_classes_by_action = {
        "default": [IsAuthenticated],
        "retrieve": [IsTeacherOrAdminUser],
        "list": [IsAdminUser],
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [
            IsAdminUser,
        ],
    }
    pagination_class = StandardResultsSetPagination

    class Meta:
        ordering = ['id']

    def list(self, request):
        school_id = request.query_params.get("school_id")
        queryset = Teacher.objects.filter(user__school=school_id)

        paginator = StandardResultsSetPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = TeacherSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            print(request.user)
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
            serializer = TeacherSerializer(
                instance, data=request.data, partial=True)

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
        "default": [IsStaffOrAdminUser],
        "retrieve": [],
        "list": [IsTeacherOrAdminUser],
        "create": [IsStaffOrAdminUser],
        "update": [],
        "partial_update": [IsStaffOrAdminUser],
        "destroy": [
            IsStaffOrAdminUser,
        ],
    }
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    class Meta:
        ordering = ['id']

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
        queryset = self.get_queryset().filter(user__school=school_id)
        paginator = StandardResultsSetPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        class_id = request.query_params.get("class_id")
        try:
            if (pk != "classid"):
                queryset = Student.objects.get(user=pk)
                serializer = StudentSerializer(queryset)
            else:
                queryset = Student.objects.filter(classe=class_id)
                serializer = StudentSerializer(queryset, many=True)

            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    pagination_class = StandardResultsSetPagination

    class Meta:
        ordering = ['id']

    def list(self, request):
        school_id = request.query_params.get("school_id")
        queryset = Parent.objects.filter(user__school=school_id)

        paginator = StandardResultsSetPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            queryset = Parent.objects.filter(student=pk)

            serializer = ParentSerializer(queryset, many=True)
            return Response(serializer.data)
        except Parent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ParentProfile(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ProfileParentSerializer

    def list(self, request):
        try:
            parent_id = request.query_params.get("parent_id")
            queryset = Parent.objects.get(user=parent_id)
            serializer = ProfileParentSerializer(queryset)
            return Response(serializer.data)
        except Parent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SubjectViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsStaffOrAdminUser]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def list(self, request):
        school_id = request.query_params.get("school_id")
        try:
            queryset = Subject.objects.filter(school=school_id)

            serializer = SubjectSerializer(queryset, many=True)
            return Response(serializer.data)
        except Subject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def list(self, request):
        school_id = request.query_params.get("school_id")
        try:
            queryset = Homework.objects.filter(school=school_id)

            serializer = HomeworkSerializer(queryset, many=True)
            return Response(serializer.data)
        except Homework.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):

        try:
            queryset = Homework.objects.filter(assigned_class=pk)

            serializer = HomeworkSerializer(queryset, many=True)
            return Response(serializer.data)
        except Homework.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ClassRoomViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsStaffOrAdminUser]
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    pagination_class = StandardResultsSetPagination

    class Meta:
        ordering = ['id']

    def list(self, request):
        
        try:
            school_id = request.query_params.get("school_id")

            queryset = ClassRoom.objects.filter(school_id=school_id)
            serializer = ClassRoomSerializer(queryset, many=True)
            return Response(serializer.data)
        except ClassRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            queryset = ClassRoom.objects.filter(assigned_teacher__user__id=pk)

            serializer = ClassRoomSerializer(queryset, many=True)
            return Response(serializer.data)
        except ClassRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PersonViewSet(viewsets.ViewSet):
    pagination_class = StandardResultsSetPagination

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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
            serializer = PersonSerializer(
                instance, data=request.data, partial=True)

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
        "create": [],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "update_device_token":[],
        "destroy": [
            IsAdminUser,
        ],
    }

    class Meta:
        ordering = ['id']

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

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SchoolMembers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=["patch"], url_path="update-device-token")
    def update_device_token(self, request, pk=None):
        """Update the device_token field for a specific SchoolMember."""
        try:
            instance = self.get_object()
            device_token = request.data.get("device_token")

            if not device_token:
                return Response(
                    {"detail": "Device token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            instance.device_token = device_token
            instance.save()
            return Response(
                {"detail": "Device token updated successfully."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ScheduleClassesViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ScheduleClassSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        school_id = request.query_params.get("school_id")
        queryset = self.queryset.model.objects.filter(
            class_room__assigned_teacher__user__school=school_id
        )

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            # Get the ClassRooms where 'classes_taught' matches the given pk
            # classrooms = ClassRoom.objects.filter(id=pk)

            # Get schedules for the filtered classrooms
            queryset = ClassSchedule.objects.filter(
                class_room__classes_taught=pk)

            if not queryset.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = ScheduleClassSerializer(queryset, many=True)
            return Response(serializer.data)
        except ClassSchedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class TeacherScheduleViewSet(viewsets.ViewSet):
    """
    A viewset to return all schedules for the classes a teacher is assigned to.
    """

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        # Get the teacher by primary key (pk)
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found."}, status=404)

        # Get the classes taught by the teacher

        # Get the schedules for the classes taught by the teacher
        schedules = ClassSchedule.objects.filter(
            class_room__assigned_teacher=teacher)

        # Serialize the data
        serializer = ClassScheduleSerializer(schedules, many=True)
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


@csrf_exempt
def password_reset_confirm(request, uid, token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        re_new_password = request.POST.get('re_new_password')

        # Validate passwords (check if they match)
        if new_password != re_new_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        # Prepare payload for Djoser's password reset confirm API
        payload = {
            'uid': uid,
            'token': token,
            'new_password': new_password,
            're_new_password': re_new_password
        }

        # Include CSRF token for security
        headers = {
            'X-CSRFToken': request.COOKIES.get('csrftoken'),
            'Content-Type': 'application/json'
        }

        # Make the request to Djoser's password reset confirm endpoint
        response = requests.post(
            f'{settings.BACKEND_API_URL}/auth/users/reset_password_confirm/', json=payload, headers=headers)

        if response.status_code == 204:  # Djoser returns 204 No Content on success
            # Return the success message to be swapped by HTMX
            return redirect("password_reset_confirmation")
        else:
            # Handle errors from the response
            print("Response status:", response.status_code)
            print("Response body:", response.json())
            error_data = response.json().get('error', 'An unexpected error occurred')
            return JsonResponse({'error': error_data}, status=response.status_code)

    # If GET request, render the password reset form
    context = {
        'uid': uid,
        'token': token,
        'csrf_token': get_token(request),
    }
    return render(request, 'auth/reset_password_confirm.html', context)


def password_reset_confirmation(request):
    return render(request, 'auth/confirmation.html')


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
        school_id = request.query_params.get("school_id")
        queryset = self.queryset.model.objects.filter(school=school_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class AttendanceView(viewsets.ModelViewSet):

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def list(self, request):
        school_id = request.query_params.get("school_id")
        queryset = self.queryset.model.objects.filter(school=school_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset.model.objects.filter(student__classe=pk)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class NotificationView(viewsets.ModelViewSet):

    queryset = Notification.objects.order_by("-timestamp")
    serializer_class = NotificationSerializer

    def list(self, request):
        school_id = request.query_params.get("school_id")
        queryset = self.queryset.model.objects.filter(sender__school=school_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        school_id = request.query_params.get("school_id")
        queryset = self.queryset.model.objects.filter(
            role=pk, sender__school=school_id
        ).order_by("-timestamp")

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)


class ResultView(viewsets.ModelViewSet):

    queryset = Result.objects.all()
    serializer_class = ResultSerializers
    permission_classes_by_action = {
        "default": [IsStaffOrAdminUser],
        "retrieve": [IsAuthenticated, ],
        "list": [IsAuthenticated],
        "create": [IsStaffOrAdminUser],
        "update": [IsStaffOrAdminUser],
        "partial_update": [IsStaffOrAdminUser],
        "destroy": [
            IsStaffOrAdminUser,
        ],
    }

    def list(self, request):

        student_id = request.query_params.get("student_id")
        queryset = self.queryset.model.objects.filter(student=student_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        student_id = request.query_params.get("student_id")
        class_id = request.query_params.get("class_id")
        print(student_id, class_id, pk)
        if (student_id != None):
            queryset = self.queryset.model.objects.filter(
                teacher=pk, student=student_id)
        elif (class_id != None):
            queryset = self.queryset.model.objects.filter(
                exam__class_association=class_id, teacher=pk)

        else:
            queryset = self.queryset.model.objects.filter(teacher=pk)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='student-result')
    def student_result(self, request):
        student_id = request.query_params.get("student_id")
        
        if not student_id:
            return Response(
                {"error": "student_ids are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            queryset = self.queryset.model.objects.filter(
                 student=student_id)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Failed Student Error.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StaffView(viewsets.ModelViewSet):

    queryset = Staff.objects.all()
    serializer_class = StaffSerialization
    permission_classes = [IsStaffOrAdminUser]
    pagination_class = StandardResultsSetPagination

    class Meta:
        ordering = ['id']

    def list(self, request):
        school_id = request.query_params.get("school_id")
        queryset = self.queryset.model.objects.filter(user__school=school_id)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StaffSerialization(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializers

    def list(self, request):
        class_id = request.query_params.get("class_id")
        teacher_id = request.query_params.get("teacher_id")
        queryset = Exam.objects.filter(
            class_association=class_id, teacher=teacher_id)
        serializer = ExamSerializers(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        teacher_id = request.query_params.get("teacher_id")

        queryset = Exam.objects.filter(
            class_association=pk
        )
        serializer = ExamSerializers(queryset, many=True)
        return Response(serializer.data)


class AttendanceChartView(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        school_id = request.query_params.get("school_id")

        attendance_data = Attendance.objects.filter(school=school_id)

        # Serialize data
        serializer = AttendancesSerializer(attendance_data, many=True)

        # Process data to get count of students present on each date
        chart_data = {}
        for attendance in serializer.data:
            date_str = attendance["date"]
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            id = attendance["id"]

            # chart_data["id"] = id
            if date in chart_data:
                chart_data[date]["num_students"] += len(attendance["student"])
            else:
                chart_data[date] = {
                    "id": attendance["id"],
                    "date": date.strftime("%Y-%m-%d"),
                    "num_students": len(attendance["student"]),
                }

        # Convert data to format suitable for chart (list of dictionaries)
        chart_data_list = [num_students for date,
                           num_students in chart_data.items()]

        return JsonResponse(chart_data_list, safe=False)

    def retrieve(self, request, pk=None):

        attendance_data = Attendance.objects.filter(teacher=pk)

        # Serialize data
        serializer = AttendancesSerializer(attendance_data, many=True)

        # Process data to get count of students present on each date
        chart_data = {}
        for attendance in serializer.data:
            date_str = attendance["date"]
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            id = attendance["id"]

            # chart_data["id"] = id
            if date in chart_data:
                chart_data[date]["num_students"] += len(attendance["student"])
            else:
                chart_data[date] = {
                    "id": attendance["id"],
                    "date": date.strftime("%Y-%m-%d"),
                    "num_students": len(attendance["student"]),
                }

        # Convert data to format suitable for chart (list of dictionaries)
        chart_data_list = [num_students for date,
                           num_students in chart_data.items()]

        return JsonResponse(chart_data_list, safe=False)


class StudentAttendance(viewsets.ModelViewSet):

    def list(self, request):
        student_id = request.query_params.get("student_id")

        response_data = calculateAttendSt(schoolId=student_id)

        return JsonResponse(response_data, safe=False)


class AllStudentsMonthlyPerformanceChartView(APIView):
    def get(self, request, school_id):
        try:
            # Filter students by the provided school
            students = Student.objects.filter(user__school=school_id)

            if not students.exists():
                return Response({"error": "No students found for this school"}, status=status.HTTP_404_NOT_FOUND)

            # Calculate monthly performance for students in this school
            performance_data = calculate_monthly_performance(students)

            return Response(performance_data, status=status.HTTP_200_OK)

        except SchoolDataModel.DoesNotExist:
            return Response({"error": "School not found"}, status=status.HTTP_404_NOT_FOUND)


class ClassMonthlyPerformanceChartView(APIView):
    def get(self, request, class_id):
        try:
            # Get students in the specified class
            students = Student.objects.filter(classe=class_id)

            if not students.exists():
                return Response({"error": "No students found for this class"}, status=status.HTTP_404_NOT_FOUND)

            # Calculate monthly performance for students in this class
            performance_data = calculate_monthly_performance(students)

            return Response({
                "class_id": class_id,
                "monthly_performance": performance_data
            }, status=status.HTTP_200_OK)

        except Classe.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)


class PerformanceView(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrAdminUser]

    def list(self, request):
        school_id = request.query_params.get("school_id")
        result_data = Result.objects.filter(exam__school=school_id)
        serializer = ResultSerializers(result_data, many=True)
        # Process data to get scores for each date
        chart_data = {}
        for result in serializer.data:
            date = result["date"]
            if date in chart_data:
                chart_data[date]["scores"].append(result["score"])
            else:
                chart_data[date] = {
                    "date": datetime.strptime(date, "%Y-%m-%d"),
                    "scores": [result["score"]],
                }

        # Calculate average score for each date
        for date, data in chart_data.items():
            average_score = sum(data["scores"]) / len(data["scores"])
            chart_data[date]["average_score"] = average_score

        # Convert data to format suitable for chart (list of dictionaries)
        chart_data_list = list(chart_data.values())

        return JsonResponse(chart_data_list, safe=False)

    def retrieve(self, request, pk=None):
        print("User Role: ", request.user.is_teacher, request.user.is_owner)

        result_data = Result.objects.filter(teacher=pk)
        serializer = ResultSerializers(result_data, many=True)
        # Process data to get scores for each date
        chart_data = {}
        for result in serializer.data:
            date = result["date"]
            if date in chart_data:
                chart_data[date]["scores"].append(result["score"])
            else:
                chart_data[date] = {
                    "date": datetime.strptime(date, "%Y-%m-%d"),
                    "scores": [result["score"]],
                }

        # Calculate average score for each date
        for date, data in chart_data.items():
            average_score = sum(data["scores"]) / len(data["scores"])
            chart_data[date]["average_score"] = average_score

        # Convert data to format suitable for chart (list of dictionaries)
        chart_data_list = list(chart_data.values())

        return JsonResponse(chart_data_list, safe=False)


class StudentByTeacherViewSet(viewsets.ViewSet):
    """
    A view to retrieve all students taught by a specific teacher.
    """

    def list(self, request):
        teacher_id = request.query_params.get("teacher_id")

        if not teacher_id:
            return Response(
                {"error": "Please provide a 'teacher_id' parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return Response(
                {"error": f"Teacher with id {teacher_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve all classes associated with the teacher via ClassRoom
        classes_taught = Classe.objects.filter(
            classrooms_taught__assigned_teacher=teacher
        ).distinct()

        if not classes_taught.exists():
            return Response(
                {"message": f"No classes assigned to teacher with id {teacher_id}."},
                status=status.HTTP_200_OK,
            )

        # Retrieve all students in those classes
        students_taught = Student.objects.filter(classe__in=classes_taught)

        if not students_taught.exists():
            return Response(
                {"message": f"No students found for teacher with id {teacher_id}."},
                status=status.HTTP_200_OK,
            )

        serializer = StudentSerializer(students_taught, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassroomByTeacherViewSet(viewsets.ViewSet):
    """
    A view to retrieve all classrooms assigned to a specific teacher.
    """

    def list(self, request):
        teacher_id = request.query_params.get("teacher_id")

        if not teacher_id:
            return Response(
                {"error": "Please provide a 'teacher_id' parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return Response(
                {"error": f"Teacher with id {teacher_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve all classrooms assigned to the teacher
        classrooms = ClassRoom.objects.filter(assigned_teacher=teacher)

        if not classrooms.exists():
            return Response(
                {"message": f"No classrooms assigned to teacher with id {teacher_id}."},
                status=status.HTTP_200_OK,
            )

        serializer = ClassRoomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FCMDeviceViewSet(viewsets.ModelViewSet):
    queryset = FCMDevice.objects.all()
    serializer_class = FCMDeviceSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='send')
    def send(self, request):
        user_id = request.data.get('user_id')
        title = request.data.get('title')
        message = request.data.get('message')

        if not user_id or not title or not message:
            return Response(
                {"error": "user_id, title, and message are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            notification = send_notification(user_id, title, message)
            return Response({"message": "Notification sent successfully!"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Failed to send notification.", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    @action(detail=False, methods=['post'], url_path='send-bulk')
    def send_bulk(self, request):
        user_ids = request.data.get('user_ids')
        title = request.data.get('title')
        message = request.data.get('message')

        if not user_ids or not isinstance(user_ids, list) or not title or not message:
            return Response(
                {"error": "user_ids (list), title, and message are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = send_bulk_notifications(user_ids, title, message)
            return Response(
                {
                    "message": "Notifications processed.",
                    "successful": result["successful"],
                    "failed": result["failed"],
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Failed to send notifications.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='send-bulk-classe')
    def send_bulk_classe(self, request):
        classe_ids = request.data.get('classe_ids')
        title = request.data.get('title')
        message = request.data.get('message')

        if not classe_ids or not isinstance(classe_ids, list) or not title or not message:
            return Response(
                {"error": "classe_ids (list), title, and message are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = send_bulk_class_notifications(classe_ids, title, message)
            return Response(
                {
                    "message": "Notifications processed.",
                    "successful": result["successful"],
                    "failed": result["failed"],
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Failed to send notifications.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 

class PubView(viewsets.ModelViewSet):
    queryset = PubModel.objects.all()
    serializer_class = PubSerializer
    pagination_class = None
    


class MonthlyPaymentViewSet(viewsets.ModelViewSet):
    queryset = MonthlyPayment.objects.all()
    serializer_class = MonthlyPaymentSerializer
    permission_classes = [IsStaffOrAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student']
    
    
    @action(detail=False, methods=['get'])
    def total_monthly_payment(self, request, *args, **kwargs):
        student_id = request.query_params.get('student')
        if not student_id:
            return Response({"error": "student_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # Calculate the total monthly payment for the student
        total_payment = MonthlyPayment.objects.filter(student=student).aggregate(
            total_amount_paid=Sum('amount_paid'),
            total_amount_due=Sum('total_amount_due')
        )

        response_data = {
            "student_id": student.id,
            "student_name": f"{student.user.person.last_name} {student.user.person.first_name}",
            "total_amount_paid": total_payment['total_amount_paid'] or 0,
            "total_amount_due": total_payment['total_amount_due'] or 0,
        }

        return Response(response_data)

    @action(detail=False, methods=['post'])
    def bulk_payment(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        start_date = request.data.get('start_date')  # Start of the payment period (e.g., "2023-12-01")
        end_date = request.data.get('end_date')  # End of the payment period (e.g., "2024-01-31")
        total_amount_paid = request.data.get('amount_paid')
        total_amount_due = request.data.get('total_amount_due', 0.0)  # Total amount due for the period

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a single payment for the date range
        payment = MonthlyPayment(
            student=student,
            amount_paid=total_amount_paid,
            total_amount_due=total_amount_due,
            start_date=start_date,
            end_date=end_date,
        )
        payment.save()

        serializer = MonthlyPaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'])
    def update_payment(self, request, pk=None):
        try:
            payment = MonthlyPayment.objects.get(pk=pk)
        except MonthlyPayment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update the payment with the provided data
        payment.amount_paid = request.data.get('amount_paid', payment.amount_paid)
        payment.total_amount_due = request.data.get('total_amount_due', payment.total_amount_due)
        payment.start_date = request.data.get('start_date', payment.start_date)
        payment.end_date = request.data.get('end_date', payment.end_date)

        payment.save()

        serializer = MonthlyPaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    pagination_class = None

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    pagination_class = None
    
    

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = None
    
    filterset_fields = ['transaction_type', 'date']
    
    @action(detail=False, methods=['get'])
    def generate_report(self, request):
        report_type = request.query_params.get('report_type')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not report_type or not start_date or not end_date:
            return Response({"error": "report_type, start_date, and end_date are required"}, status=400)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        # Calculate total income (fee payments)
        
        total_income = Transaction.objects.filter(
            transaction_type='Fee Payment',
            date__range=[start_date, end_date]
        ).aggregate(total_income=Sum('amount'))['total_income'] or 0

        # Calculate total expenses (expense payments)
        
        total_expenses = Transaction.objects.filter(
            transaction_type='Expense Payment',
            date__range=[start_date, end_date]
        ).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0
         
        # Create the financial report
        report = FinancialReport.objects.create(
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            total_income=total_income,
            total_expenses=total_expenses
        )

        serializer = FinancialReportSerializer(report)
        return Response(serializer.data)

class FinancialReportViewSet(viewsets.ModelViewSet):
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
    pagination_class = None
    

class StudentLightView(viewsets.ModelViewSet):
    
    queryset = Student.objects.all()
    serializer_class = StudentLightSerializer
    pagination_class = None
    
    def list(self, request):
        school_id = request.query_params.get("school_id")

        if not school_id:
            return Response(
                {"error": "Please provide a 'school_id' parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            students = Student.objects.filter(classe__school=school_id)
        except Student.DoesNotExist:
            return Response(
                {"error":  "Student with  does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        serializer = StudentLightSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)