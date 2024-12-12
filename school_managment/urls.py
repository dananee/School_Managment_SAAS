from django.urls import path, include


from .views import (
    AllStudentsMonthlyPerformanceChartView,
    AttendanceChartView,
    AttendanceView,
    ClassMonthlyPerformanceChartView,
    ClassRoomViewSet,
    ClassViewSet,
    EventsView,
    ExamViewSet,
    FCMDeviceViewSet,
    MyTokenObtainPairView,
    NotificationView,
    ParentViewSet,
    PerformanceView,
    PersonViewSet,
    ResultView,
    ScheduleClassesViewSet,
    SchoolDataView,
    SchoolMembersViewSet,
    StaffView,
    StudentByTeacherViewSet,
 ParentProfile,
    StudentViewSet,
    SubjectViewSet,
    TeacherScheduleViewSet,
    TeacherViewSet,
    StudentAttendance,
    HomeworkViewSet,
   
   
    
)


from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"school_data", SchoolDataView)

router.register(r'teschedule', TeacherScheduleViewSet, basename='teacher-schedule')

router.register(r"classes", ClassViewSet)
router.register(r"student_attend", StudentAttendance,basename='attendance-student')
router.register(r"homework", HomeworkViewSet,basename='homework')
router.register(r"events", EventsView)
router.register(r"teachers", TeacherViewSet)
router.register(r"student", StudentViewSet)
router.register(r"parentp", ParentProfile)
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
router.register(r"exam", ExamViewSet, basename="exams")
router.register(r"performence", PerformanceView, basename="perform-chart")
router.register(r"attedchart", AttendanceChartView, basename="attend-chart")
router.register(r"testudent", StudentByTeacherViewSet, basename="filter-student")
router.register(r'fcm-devices', FCMDeviceViewSet, basename='fcmdevice')


urlpatterns = [
        # path('send-notification/', send_notification, name='send-notification'),
 path('students/<int:school_id>/monthly-performance-chart/', AllStudentsMonthlyPerformanceChartView.as_view(), name='all-students-monthly-performance-chart'),
    path('classes/<int:class_id>/monthly-performance-chart/', ClassMonthlyPerformanceChartView.as_view(), name='class-monthly-performance-chart'),
   
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
 
 
    path("", include(router.urls)),
]


