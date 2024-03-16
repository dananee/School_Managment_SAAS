from django.db import models
from django.utils.translation import gettext_lazy as _
from django_mysql.models import ListCharField
import json
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.hashers import make_password


def upload_to(instance, filename):
    return f'images/{filename}'


class Genders(models.TextChoices):
    MEN = "M", _('MEN')
    FEMALE = "F", _('FEMALE')


class EducationStage(models.TextChoices):
    ELMENTARY = "EL", _('ELMENTARY')
    PRIMARY = "PR", _('PRIMARY')
    LYCEE = "LY", _('LYCEE')
    UNIVERSITY = "UN", _('UNIVERSITY')


class Roles(models.TextChoices):
    OWNER = "OW", _('OWNER')
    STAFF = "SF", _('STAFF')
    TEACHER = "TE", _('TEACHER')
    STUDENT = "ST", _('STUDENT')
    PARENT = "PT", _('PARENT')


class SchoolDataModel(models.Model):

    name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=200)
    logo_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    education_stage = ListCharField(
        base_field=models.CharField(
            max_length=2, choices=EducationStage, default=EducationStage.PRIMARY),
        size=4,
        default=EducationStage.PRIMARY,
        max_length=(4 * 3)  # 6 * 10 character nominals, plus commas
    )

    class Meta:
        db_table = "school_data_tb"
        verbose_name = "School Data"
        verbose_name_plural = "School Data"

    def __str__(self) -> str:
        return f'{self.id} - {self.name}'


class PersonManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
         

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.password = make_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password=password
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
         
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser):
    # person_id = 
    last_login = models.DateTimeField(auto_now_add=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=200, null=False)
    
    gender = models.CharField(
        max_length=1, choices=Genders, default=Genders.MEN)
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Add is_staff field
    is_superuser = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True,null=True)
    objects = PersonManager()
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'Person'
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self) -> str:
        return f"{self.id} - {self.email}"


class SchoolMembers(models.Model):

     
    profile_image = models.ImageField(
        upload_to=upload_to, blank=True, null=True)
    role = models.CharField(
        max_length=2, choices=Roles, default=Roles.STAFF)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'SchoolMembers'
        verbose_name = 'SchoolMember'
        verbose_name_plural = 'SchoolMembers'

    def __str__(self) -> str:
        return f"{self.person.first_name} {self.person.last_name}  - {self.role} - {self.school}"


class Admin(models.Model):
    # Admin-specific fields
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.user_id} - {self.user.person.last_name} - {self.user.school.name}'


class Student(models.Model):
    # Student-specific fields
     
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE)
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self) -> str:
        return f'{self.user.user_id} - {self.user.person.email}'


class Parent(models.Model):
    # Parent-specific fields
     
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Parent'
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'

    def __str__(self) -> str:
        return f'{self.user.user_id} - '


class Staff(models.Model):
    # Staff-specific fields
   
    position = models.CharField(max_length=255)
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Staff'
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'

    def __str__(self) -> str:
        return f'{self.user.person.last_name} - {self.position}'


class Classe(models.Model):
    
    class_name = models.CharField(max_length=200, null=False, blank=False)
    grade = models.CharField(max_length=200, null=False, blank=False)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
         
        db_table = 'Classe'
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'

    def __str__(self) -> str:
        return f'{self.school.name} - {self.class_name} {self.grade}'


class Teacher(models.Model):
    
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255, null=False, blank=False)
    experience = models.IntegerField(null=False, blank=False)
    specialization = models.CharField(max_length=255, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    joining_date = models.DateField(auto_now_add=True)
    teaching_classes = models.ManyToManyField(
        Classe, related_name='teachers', blank=False)

    class Meta:
        db_table = 'Teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.user.person.email}'s Profile"


class Subject(models.Model):
    
    subject_name = models.CharField(max_length=255)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'Subject'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self) -> str:
        return f'{self.school.name} - {self.subject_name}'


class Attendance(models.Model):
    
    date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True,blank=False)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self) -> str:
        return f'{self.school.name} - {self.student}'

    class Meta:
        unique_together = ('date', 'student')
        db_table = 'Attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'


class Grade(models.Model):
     
    grade = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Grade'
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'


class Exam(models.Model):
     
    date = models.DateField()
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)
    class_association = models.ForeignKey(
        Classe, on_delete=models.CASCADE, null=True)
    subject_association = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Exam'
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'

    # Additional fields, relationships, if needed


class Result(models.Model):
     
    score = models.FloatField()
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    # Additional fields, relationships, if needed

    class Meta:
        db_table = 'Result'
        verbose_name = 'Result'
        verbose_name_plural = 'Results'


class ClassRoom(models.Model):
 
    room_name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    building = models.CharField(max_length=255, null=True, blank=True)
    is_virtual = models.BooleanField(default=False)
    classes_taught = models.ManyToManyField(
        Classe, related_name='classrooms_taught', blank=True)
    assigned_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    subjects_taught = models.ForeignKey(
        Subject, related_name='classrooms_taught',on_delete=models.SET_NULL, blank=True,null=True)
    # Add other fields specific to the ClassRoom model if needed
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'ClassRoom'
        verbose_name = 'Classe Room'
        verbose_name_plural = 'Classe Rooms'

    def __str__(self):
        return f"{self.room_name}  "


class ClassSchedule(models.Model):
    
    day = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)
    # Add other fields specific to the ClassSchedule model if needed

    class Meta:
        db_table = 'ClassSchedule'
        verbose_name = 'Classe Schedule'
        verbose_name_plural = 'Classe Schedules'

    def __str__(self):
        return f"{self.day} | {self.start_time} - {self.end_time} | Room: {self.class_room}"


class Events(models.Model):

    event_name = models.CharField(max_length=200,blank=False,null=False)
    desricption = models.TextField(max_length=300,blank=True,default='no description')
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    color = models.CharField(max_length=12)
    is_all_day = models.BooleanField(default=False)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.event_name} - {self.school}"
    


class NotificationModel(models.Model):

     
    sender = models.ForeignKey(SchoolMembers,on_delete=models.CASCADE)
    message = models.CharField(max_length=255,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.id} - {self.sender}"
 