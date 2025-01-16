from django.contrib import admin

from .models import ClassRoom, Expense, FeeStructure, FinancialReport, Homework, ClassSchedule, Events, FCMDevice, MonthlyPayment, Notification, PubModel, SchoolDataModel, Teacher, SchoolMembers, Person, Student, Parent, Admin, Staff, Classe, Exam, Result, Attendance, Subject, Transaction
# Register your models here.
admin.autodiscover()
admin.site.enable_nav_sidebar = True

admin.site.register(SchoolDataModel)
admin.site.register(SchoolMembers)
admin.site.register(Person)
admin.site.register(Parent)
admin.site.register(Admin)
admin.site.register(Attendance)
admin.site.register(Classe)
admin.site.register(Exam)
admin.site.register(Result)
admin.site.register(Subject)
admin.site.register(PubModel)

admin.site.register(ClassRoom)
admin.site.register(ClassSchedule)
admin.site.register(Events)
admin.site.register(Notification)
admin.site.register(Homework)
admin.site.register(FCMDevice)

admin.site.register(FeeStructure)
admin.site.register(Expense)
admin.site.register(Transaction)
admin.site.register(FinancialReport)
admin.site.register(MonthlyPayment)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'qualification',
                    'experience', 'specialization', 'joining_date')
    list_filter = ('qualification', 'experience', 'joining_date')
    search_fields = ('user__person__first_name', 'user__person__last_name',
                     'specialization', 'user__person__email')
    ordering = ('-joining_date',)
    readonly_fields = ('joining_date',)

    fieldsets = (
        ('Personal Info', {
            'fields': ('user', 'qualification', 'experience', 'specialization', 'address')
        }),
        ('Important Dates', {
            'fields': ('joining_date',),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.person.email if obj.user and obj.user.person else "N/A"


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'get_email', 'position',
                    )

    search_fields = ('user__person__first_name', 'user__person__last_name',
                     'position', 'user__person__email')

    fieldsets = (
        ('Personal Info', {
            'fields': ('user', 'position',)
        }),
        
    )

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.person.email if obj.user and obj.user.person else "N/A"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'get_email', 'get_classe_name', 'get_classe_grade')
    list_filter = ('classe__grade', 'classe__class_name')
    search_fields = ('user__person__first_name', 'user__person__last_name',
                     'user__person__email')

    fieldsets = (
        ('Personal Info', {
            'fields': ('user',)
        }),
       
    )
    
     

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.person.email if obj.user and obj.user.person else "N/A"

    @admin.display(description='Class Name')
    def get_classe_name(self, obj):
        return obj.classe.class_name if obj.classe else "N/A"

    @admin.display(description='Grade')
    def get_classe_grade(self, obj):
        return obj.classe.grade if obj.classe else "N/A"
