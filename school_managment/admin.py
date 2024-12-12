from django.contrib import admin

from  .models import ClassRoom,Homework, ClassSchedule, Events, FCMDevice, Notification, SchoolDataModel, Teacher,SchoolMembers,Person,Student,Parent,Admin,Staff,Classe,Exam,Result,Attendance,Subject
# Register your models here.
admin.autodiscover()
admin.site.enable_nav_sidebar = True

admin.site.register(SchoolDataModel)
admin.site.register(SchoolMembers)
admin.site.register(Person)
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(Attendance)
admin.site.register(Classe)
admin.site.register(Exam)
admin.site.register(Result)
admin.site.register(Staff)
admin.site.register(Subject)
 
admin.site.register(ClassRoom)
admin.site.register(ClassSchedule)
admin.site.register(Events)
admin.site.register(Notification)
admin.site.register(Homework)
admin.site.register(FCMDevice)


@admin.register(Teacher)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ("user", "joining_date","experience")
    search_fields = ("first_name",)