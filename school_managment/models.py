from django.db import models
from django.utils.translation import gettext_lazy as _
from django_mysql.models import ListCharField
import json
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
import os
from django.core.exceptions import ValidationError
from decimal import Decimal

def upload_to(instance, filename):
    return f"images/{filename}"

def upload_to_pub(instance, filename):
    return f"images/pub/{filename}"

class Genders(models.TextChoices):
    MEN = "M", _("MEN")
    FEMALE = "F", _("FEMALE")


class Status(models.TextChoices):
    WARNING = "WR", _("WARNING")
    IMPORTANT = "IM", _("IMPORTANT")
    EVENT = "EV", _("EVENT")


class EducationStage(models.TextChoices):
    ELMENTARY = "EL", _("ELMENTARY")
    PRIMARY = "PR", _("PRIMARY")
    LYCEE = "LY", _("LYCEE")
    UNIVERSITY = "UN", _("UNIVERSITY")


class Roles(models.TextChoices):
    OWNER = "OW", _("OWNER")
    STAFF = "SF", _("STAFF")
    TEACHER = "TE", _("TEACHER")
    STUDENT = "ST", _("STUDENT")
    PARENT = "PT", _("PARENT")


class SchoolDataModel(models.Model):

    name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=200)
    logo_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    education_stage = ListCharField(
        base_field=models.CharField(
            max_length=2, choices=EducationStage, default=EducationStage.PRIMARY
        ),
        size=4,
        default=EducationStage.PRIMARY,
        max_length=(4 * 3),  # 6 * 10 character nominals, plus commas
    )

    class Meta:
        db_table = "school_data_tb"
        verbose_name = "School Data"
        verbose_name_plural = "School Data"

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"


class PersonManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.password = make_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password)

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
    phone = PhoneNumberField(null=True, blank=True, unique=False)

    gender = models.CharField(
        max_length=1, choices=Genders, default=Genders.MEN)
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Add is_staff field
    is_superuser = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True, null=True)
    objects = PersonManager()
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "Person"
        verbose_name = "Person"
        verbose_name_plural = "People"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self) -> str:
        return f"{self.id} - {self.email}"


class SchoolMembers(models.Model):

    profile_image = models.ImageField(
        upload_to=upload_to, blank=True, null=True)
    role = models.CharField(max_length=2, choices=Roles, default=Roles.STAFF)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True)
    device_token = models.CharField(max_length=255, blank=True, null=True)  # Add this field


    class Meta:
        db_table = "SchoolMembers"
        verbose_name = "SchoolMember"
        verbose_name_plural = "SchoolMembers"
        
        
    def save(self, *args, **kwargs):
        # Check if the instance already exists in the database
        if self.pk:
            # Get the existing instance from the database
            old_instance = SchoolMembers.objects.get(pk=self.pk)
            # Check if the image has changed
            if old_instance.profile_image and old_instance.profile_image != self.profile_image:
                # Delete the old image file
                old_image_path = os.path.join(settings.MEDIA_ROOT, old_instance.profile_image.name)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
        # Call the parent class's save method
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.profile_image.name)
            if os.path.exists(image_path):
                os.remove(image_path)
        # Call the parent class's delete method
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.person.first_name} {self.person.last_name}"



class Admin(models.Model):
    # Admin-specific fields
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return (
            f"{self.user.id} - {self.user.person.last_name} - {self.user.school.name}"
        )


class Student(models.Model):
    # Student-specific fields
    classe = models.ForeignKey("Classe", on_delete=models.CASCADE)
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)
    
    
    class Meta:
        db_table = "Student"
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self) -> str:
        return f"{self.user.id} - {self.user.person.email}"


class Parent(models.Model):
    student = models.ManyToManyField(
        Student, related_name="parents", blank=True, default=[])
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    class Meta:
        db_table = "Parent"
        verbose_name = "Parent"
        verbose_name_plural = "Parents"

    def __str__(self) -> str:
        return f"{self.user.id} -  "


class Staff(models.Model):
    # Staff-specific fields

    position = models.CharField(max_length=255)
    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)

    class Meta:
        db_table = "Staff"
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"

    def __str__(self) -> str:
        return f"{self.user.person.last_name} - {self.position}"


class Classe(models.Model):

    class_name = models.CharField(max_length=200, null=False, blank=False)
    grade = models.CharField(max_length=200, null=False, blank=False)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=False, blank=False
    )

    class Meta:

        db_table = "Classe"
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

    def __str__(self) -> str:
        return f"{self.id} -> {self.school.name} - {self.class_name} {self.grade}"


class Teacher(models.Model):

    user = models.OneToOneField(SchoolMembers, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255, null=False, blank=False)
    experience = models.IntegerField(null=False, blank=False)
    specialization = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    joining_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['joining_date']
        db_table = "Teacher"
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return f"{self.id} -> {self.user.person.email} - {self.user.person.last_name}"


class Subject(models.Model):

    subject_name = models.CharField(max_length=255)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "Subject"
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self) -> str:
        return f"{self.id} - {self.subject_name}"


class Homework(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    assigned_by = models.ForeignKey(
        # Assuming teacher is a user
        Teacher, on_delete=models.CASCADE, null=True, blank=True)
    assigned_class = models.ForeignKey(Classe, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    school = school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.title} -> {self.assigned_class}"


class Attendance(models.Model):

    date = models.DateTimeField(auto_now_add=True)
    schedule = models.ForeignKey(
        "ClassSchedule", on_delete=models.CASCADE, null=True, blank=False
    )
    student = models.ManyToManyField(
        Student, related_name="student", blank=False)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=False, blank=False
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.date} - {self.school}"

    class Meta:

        db_table = "Attendance"
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"


class Grade(models.Model):

    grade = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "Grade"
        verbose_name = "Grade"
        verbose_name_plural = "Grades"


class Exam(models.Model):

    date = models.DateField()
    exam_name = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True, blank=True
    )
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True
    )
    class_association = models.ForeignKey(
        Classe, on_delete=models.CASCADE, null=True)
    subject_association = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True
    )

    class Meta:
        db_table = "Exam"
        verbose_name = "Exam"
        verbose_name_plural = "Exams"

    def __str__(self):
        return f"{self.exam_name} - {self.teacher}"

    # Additional fields, relationships, if needed


class Result(models.Model):

    date = models.DateField(auto_now_add=True)
    score = models.FloatField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False)
    # Additional fields, relationships, if needed

    def __str__(self) -> str:
        return f"{self.exam.exam_name} - {self.student}"

    class Meta:
        db_table = "Result"
        verbose_name = "Result"
        verbose_name_plural = "Results"


class ClassRoom(models.Model):

    room_name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    building = models.CharField(max_length=255, null=True, blank=True)
    is_virtual = models.BooleanField(default=False)
    classes_taught = models.ForeignKey(
        Classe, related_name="classrooms_taught", on_delete=models.CASCADE, null=True, blank=True
    )
    assigned_teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True, blank=True
    )
    subjects_taught = models.ForeignKey(
        Subject,
        related_name="classrooms_taught",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "ClassRoom"
        verbose_name = "Classe Room"
        verbose_name_plural = "Classe Rooms"

    def __str__(self):
        return f"{self.room_name} {self.assigned_teacher.user.person.email} "


class ClassSchedule(models.Model):
    day = models.CharField(
        max_length=10,
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
            ("Sunday", "Sunday"),
        ],
    )
    start_time = models.TimeField(help_text="Enter time in HH:mm format")
    end_time = models.TimeField(help_text="Enter time in HH:mm format")
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "ClassSchedule"
        verbose_name = "Class Schedule"
        verbose_name_plural = "Class Schedules"
        constraints = [
            models.UniqueConstraint(
                fields=['day', 'start_time', 'end_time', 'class_room'],
                name='unique_schedule_per_room_per_day_per_time'
            )
        ]

    def __str__(self):
        return f"{self.day} | {self.start_time} - {self.end_time} | Room: {self.class_room}"

    def clean(self):
        # Check for overlapping schedules for the same classroom on the same day
        overlapping_schedules = ClassSchedule.objects.filter(
            day=self.day,
            class_room=self.class_room,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)  # Exclude the current instance if updating

        if overlapping_schedules.exists():
            raise ValidationError("A schedule with overlapping time already exists for this classroom on the same day.")

    def save(self, *args, **kwargs):
        self.clean()  # Run validation before saving
        super().save(*args, **kwargs)


class Events(models.Model):

    event_name = models.CharField(max_length=200, blank=False, null=False)
    desricption = models.TextField(
        max_length=300, blank=True, default="no description")
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    color = models.CharField(max_length=12)
    is_all_day = models.BooleanField(default=False)
    school = models.ForeignKey(
        SchoolDataModel, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:

        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self) -> str:
        return f"{self.event_name} - {self.school}"


class Notification(models.Model):
    role = models.CharField(max_length=2, choices=Roles, default=Roles.STAFF)
    sender = models.ForeignKey(SchoolMembers, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.IMPORTANT
    )
    read = models.BooleanField(default=False)

    class Meta:
        db_table = "Notification"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self) -> str:
        return f"{self.id} - {self.sender} - {self.role}"


class FCMDevice(models.Model):
    user = models.ForeignKey(SchoolMembers, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token

class PubModel(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to=upload_to_pub, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Check if the instance already exists in the database
        if self.pk:
            # Get the existing instance from the database
            old_instance = PubModel.objects.get(pk=self.pk)
            # Check if the image has changed
            if old_instance.image and old_instance.image != self.image:
                # Delete the old image file
                old_image_path = os.path.join(settings.MEDIA_ROOT, old_instance.image.name)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
        # Call the parent class's save method
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.exists(image_path):
                os.remove(image_path)
        # Call the parent class's delete method
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title



class MonthlyPayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Partial', 'Partial'),
        ('Paid', 'Paid'),
    ]

    student = models.ForeignKey(
        'Student', 
        on_delete=models.CASCADE, 
        
    )
    amount_paid = models.DecimalField(max_digits=50, decimal_places=4)  # Amount actually paid
    total_amount_due = models.DecimalField(max_digits=50, decimal_places=4)  # Total amount due for the period
    start_date = models.DateField()  # Start of the payment period
    end_date = models.DateField()  # End of the payment period
    payment_date = models.DateField(auto_now_add=True)  # Date when the payment was made
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    class Meta:
        ordering = ['payment_date']
        
    def __str__(self):
        return f"{self.student.id} - {self.start_date} to {self.end_date} - {self.status}"

    def save(self, *args, **kwargs):
        # Automatically update the status based on the amount paid
        if Decimal(self.amount_paid) >= Decimal(self.total_amount_due):
            self.status = 'Paid'
        elif Decimal(self.amount_paid) > 0.0:
            self.status = 'Partial'
        else:
            self.status = 'Pending'
        super().save(*args, **kwargs)


class FeeStructure(models.Model):
     
    classe_fee = models.OneToOneField(
        Classe,on_delete=models.CASCADE, null=True,unique=True,blank=True
    )
    tuition_fee = models.DecimalField(max_digits=50, decimal_places=4) # Tuition fee
    activity_fee = models.DecimalField(max_digits=50,decimal_places=4)  # Activity fee
    transportation_fee = models.DecimalField(max_digits=50,decimal_places=4)  # Transportation fee
    other_fee = models.DecimalField(max_digits=50,decimal_places=4)  # Other fees
    total_fee = models.DecimalField(max_digits=50,decimal_places=4, editable=False)  # Automatically calculated

    def save(self, *args, **kwargs):
        # Automatically calculate the total fee
        self.total_fee = self.tuition_fee + self.activity_fee + self.transportation_fee + self.other_fee
        super().save(*args, **kwargs)

     
    def __str__(self):
        return f"{self.classe_fee.class_name} - Total Fee: {self.total_fee}"

class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('Salary', 'Salary'),
        ('Utilities', 'Utilities'),
        ('Maintenance', 'Maintenance'),
        ('Supplies', 'Supplies'),
        ('Other', 'Other'),
    ]

    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)  # Expense category
    description = models.CharField(max_length=200)  # Description of the expense
    amount = models.DecimalField(max_digits=50, decimal_places=4)  # Amount spent
    date = models.DateField()  # Date of the expense

    def __str__(self):
        return f"{self.category} - {self.description} - {self.amount}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Fee Payment', 'Fee Payment'),
        ('Expense Payment', 'Expense Payment'),
    ]

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)  # Type of transaction
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)  # For fee payments
    expense = models.ForeignKey('Expense', on_delete=models.SET_NULL, null=True, blank=True)  # For expense payments
    amount = models.DecimalField(max_digits=50, decimal_places=4)  # Transaction amount
    date = models.DateField(auto_now_add=True)  # Date of the transaction

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.date}"

class FinancialReport(models.Model):
    REPORT_TYPES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annual', 'Annual'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)  # Type of report
    start_date = models.DateField()  # Start date of the report period
    end_date = models.DateField()  # End date of the report period
    total_income = models.DecimalField(max_digits=50, decimal_places=4, default=0)  # Total income
    total_expenses = models.DecimalField(max_digits=50, decimal_places=4, default=0)  # Total expenses
    balance = models.DecimalField(max_digits=50, decimal_places=4, editable=False)  # Automatically calculated

    
    def save(self, *args, **kwargs):
        # Automatically calculate the balance
        self.balance = self.total_income - self.total_expenses
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.report_type} Report - Balance: {self.balance}"