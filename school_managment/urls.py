from django.urls import path, include


from .views import (
    AttendanceView,
    ClassRoomViewSet,
    ClassViewSet,
    EventsView,
    ExamViewSet,
    MyTokenObtainPairView,
    NotificationView,
    ParentViewSet,
    PersonViewSet,
    ResultView,
    ScheduleClassesViewSet,
    SchoolDataView,
    SchoolMembersViewSet,
    StaffView,
    StudentPerformanceViewSet,
    StudentViewSet,
    SubjectViewSet,
    TeacherViewSet,
)


from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"school_data", SchoolDataView)


router.register(r"classes", ClassViewSet)
router.register(r"events", EventsView)
router.register(r"teachers", TeacherViewSet)
router.register(r"student", StudentViewSet)
router.register(r"parent", ParentViewSet)
router.register(r"subjects", SubjectViewSet)
router.register(r"classrooms", ClassRoomViewSet)
router.register(r"persons", PersonViewSet, basename="person")
router.register(r"school_members", SchoolMembersViewSet)
router.register(r"class_schedule", ScheduleClassesViewSet)
router.register(r"attendace", AttendanceView)
router.register(r"notification", NotificationView)
router.register(r"staff", StaffView)
router.register(r"result", ResultView)
router.register(r"perform", StudentPerformanceViewSet, basename="performance")
router.register(r"exam", ExamViewSet, basename="exams")

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("", include(router.urls)),
]
