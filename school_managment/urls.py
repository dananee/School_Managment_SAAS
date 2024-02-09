from django.urls import path, include


from .views import ClassRoomViewSet, ClassViewSet, MyTokenObtainPairView,  PersonViewSet, ScheduleClassesViewSet, SchoolDataView, SchoolMembersViewSet, SubjectViewSet, TeacherViewSet


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


    path("", include(router.urls)),

]
