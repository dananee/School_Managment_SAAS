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
    ExpenseViewSet,
    FeeStructureViewSet,
    FinancialReportViewSet,
    MonthlyPaymentViewSet,
   
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
    StudentLightView,
    StudentViewSet,
    SubjectViewSet,
    TeacherLightViewSet,
    TeacherScheduleViewSet,
    TeacherViewSet,
    StudentAttendance,
    HomeworkViewSet,
PubView,
NotificationViewSet,
    ClassroomByTeacherViewSet,
    TransactionViewSet
)


from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"school_data", SchoolDataView)

router.register(r'teschedule', TeacherScheduleViewSet,
                basename='teacher-schedule')

router.register(r"classes", ClassViewSet)
router.register(r"student_attend", StudentAttendance,
                basename='attendance-student')
router.register(r"homework", HomeworkViewSet, basename='homework')
router.register(r"events", EventsView)
router.register(r"teachers", TeacherViewSet)
router.register(r"teachers-light", TeacherLightViewSet)
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
router.register(r"testudent", StudentByTeacherViewSet,
                basename="filter-student")
router.register(r"classrooms-by-teacher",
                ClassroomByTeacherViewSet, basename="filter-student")
router.register(r'fcm-devices', NotificationViewSet, basename='fcmdevice')
router.register(r'pubs', PubView, basename='publications')

router.register(r'monthly-payments', MonthlyPaymentViewSet, basename='monthlypayment')
router.register(r'fee-structures', FeeStructureViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'financial-reports', FinancialReportViewSet)
router.register(r'students-light', StudentLightView)

urlpatterns = [
    # path('send-notification/', send_notification, name='send-notification'),
    path('students/<int:school_id>/monthly-performance-chart/',
         AllStudentsMonthlyPerformanceChartView.as_view(), name='all-students-monthly-performance-chart'),
    path('classes/<int:class_id>/monthly-performance-chart/',
         ClassMonthlyPerformanceChartView.as_view(), name='class-monthly-performance-chart'),

    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),


    path("", include(router.urls)),
]
