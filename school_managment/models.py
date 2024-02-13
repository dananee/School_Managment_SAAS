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
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser):
    # person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=200, null=False)
    profile_image = models.ImageField(
        upload_to=upload_to, blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=Genders, default=Genders.MEN)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Add is_staff field
    is_superuser = models.BooleanField(default=False)

    objects = PersonManager()
    USERNAME_FIELD = 'email'

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='person_groups'  # Unique related_name for Person model groups
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='person_permissions'  # Unique related_name for Person model
    )

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

    user_id = models.AutoField(primary_key=True)
    role = models.CharField(
        max_length=2, choices=Roles, default=Roles.STAFF)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'SchoolMembers'
        verbose_name = 'SchoolMember'
        verbose_name_plural = 'SchoolMembers'

    def __str__(self) -> str:
        return f"{self.person.last_name}  - {self.role}"


class Admin(models.Model):
    # Admin-specific fields
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.user_id} - {self.user.username}'


class Student(models.Model):
    # Student-specific fields
    student_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE)
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self) -> str:
        return f'{self.user.user_id} - {self.user.username}'


class Parent(models.Model):
    # Parent-specific fields
    parent_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Parent'
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'

    def __str__(self) -> str:
        return f'{self.user.user_id} - {self.user.username}'


class Staff(models.Model):
    # Staff-specific fields
    staff_id = models.AutoField(primary_key=True)
    position = models.CharField(max_length=255)
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Staff'
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'

    def __str__(self) -> str:
        return f'{self.user.person.last_name} - {self.position}'


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=255)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('class_name', 'school')

    def __str__(self) -> str:
        return f'{self.school.name} - {self.class_name}'


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    teaching_classes = models.ManyToManyField(
        Class, related_name='teachers', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.school.name} - {self.subject_name}'


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.school.name} - {self.student}'

    class Meta:
        unique_together = ('date', 'student')


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    grade = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)


class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    date = models.DateField()
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True)
    class_association = models.ForeignKey(
        Class, on_delete=models.CASCADE, null=True)
    subject_association = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True)

    # Additional fields, relationships, if needed


class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    score = models.FloatField()
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    # Additional fields, relationships, if needed


class ClassRoom(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    building = models.CharField(max_length=255, null=True, blank=True)
    is_virtual = models.BooleanField(default=False)
    classes_taught = models.ManyToManyField(
        Class, related_name='classrooms_taught', blank=True)
    assigned_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    subjects_taught = models.ManyToManyField(
        Subject, related_name='classrooms_taught', blank=True)
    # Add other fields specific to the ClassRoom model if needed

    def __str__(self):
        return self.room_name


class ClassSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
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
    # Add other fields specific to the ClassSchedule model if needed

    def __str__(self):
        return f"{self.day} | {self.start_time} - {self.end_time} | Room: {self.class_room}"
