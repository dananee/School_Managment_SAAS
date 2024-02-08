from django.urls import path, include

 

from .views import ClassRoomViewSet, ClassViewSet, MyTokenObtainPairView, PasswordResetConfirmView, PasswordResetView, PersonViewSet, ScheduleClassesViewSet, SchoolDataView, SchoolMembersViewSet, SubjectViewSet, TeacherViewSet


from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'school_data', SchoolDataView)
router

router.register(r'classes', ClassViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'classrooms', ClassRoomViewSet)
router.register(r'persons', PersonViewSet, basename='person')
router.register(r'school_members', SchoolMembersViewSet)
router.register(r'class_schedule', ScheduleClassesViewSet)

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("", include(router.urls)),

]
