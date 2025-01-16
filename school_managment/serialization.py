# Adjust this import to your actual User model
 
 
from school_managment.models import Person
import json
from rest_framework import serializers
from .models import (
    Attendance,
    ClassSchedule,
    Events,
    Exam,
    Expense,
    FCMDevice,
    FeeStructure,
    FinancialReport,
    Notification,
    Parent,
    Result,
    SchoolDataModel,
    Genders,
    Classe,
    SchoolMembers,
    Staff,
    Student,
    Teacher,
    Subject,
    ClassRoom,
    Person,
    Homework,
    PubModel,
    MonthlyPayment,
    Transaction
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import (
    PasswordResetConfirmSerializer as DjoserPasswordResetConfirmSerializer,
)

from phonenumber_field.serializerfields import PhoneNumberField
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.db.models.functions import TruncMonth


def calculate_monthly_performance(student):
    # Filter results by student and group by month

    if not student.exists():
        return []

    monthly_performance = (
        Result.objects.filter(student__in=student)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(average_score=Avg('score'))
        .order_by('month')
    )

    # Convert to a dictionary format or list of tuples for further use
    performance_data = [
        {"date": entry['month'], "average_score": entry['average_score']}
        for entry in monthly_performance
    ]

    return performance_data


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if "data:" in data and ";base64," in data:
                # Break out the header from the base64 content
                header, data = data.split(";base64,")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            # Generate file name:
            # 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (
                file_name,
                file_extension,
            )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

#Acounting
class FeeStructureSerializer(serializers.ModelSerializer):
    classe_fee_id = serializers.PrimaryKeyRelatedField(
        queryset=Classe.objects.all(), source='classe_fee', write_only=True)
    
    class Meta:
        model = FeeStructure
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['classe_fee'] = ClassSerializer(instance.classe_fee).data
        
        return representation
    
    def validate(self, data):
        classe_fee = data.get('classe_fee')
        if classe_fee:  # Check if classe_fee is provided
            # Check if a FeeStructure with this classe_fee already exists
            if FeeStructure.objects.filter(classe_fee=classe_fee).exists():
                raise serializers.ValidationError({
                    'error':'free structure for this classd already exists.'
                })
        return data
        
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source="student", write_only=True, allow_null=True
    )
    
    expense_id = serializers.PrimaryKeyRelatedField(
        queryset=Expense.objects.all(), source="expense", write_only=True, allow_null=True
    )
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.student != None:
            representation["student"] = StudentLightSerializer(instance.student).data
        else:
            representation["student"] = None
        
        if instance.expense != None:
            representation["expense"] = ExpenseSerializer(instance.expense).data
        else:
            representation["expense"] = None
        return representation
    
    class Meta:
        model = Transaction
        fields = '__all__'

class FinancialReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialReport
        fields = '__all__'
        
class MonthlyPaymentSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source="student", write_only=True, allow_null=True
    )
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.student != None:
            representation["student"] = StudentLightSerializer(instance.student).data
        return representation
    
    class Meta:
        model = MonthlyPayment
        fields =  "__all__"


       
class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    re_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        uid = data.get('uid')
        token = data.get('token')
        new_password = data.get('new_password')
        re_new_password = data.get('re_new_password')

        # Ensure passwords are present
        if not new_password or not re_new_password:
            raise serializers.ValidationError(
                "Both new password and confirm password are required.")

        # Validate if passwords match
        if new_password != re_new_password:
            raise serializers.ValidationError("Passwords do not match.")

        # Decode the UID to get the user
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = Person.objects.get(pk=uid)  # Adjust to your User model
            print(f"Decoded UID: {uid}, User: {user}")
        except (Person.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError("Invalid user ID.")

        # Validate the token
        if not default_token_generator.check_token(user, token):
            print(f"Invalid token: {token}")
            raise serializers.ValidationError("Invalid or expired token.")

        # Save the user to be used in the save method
        self.user = user
        return data

    def save(self, **kwargs):
        # Now access the new_password from validated_data
        new_password = self.validated_data["new_password"]

        # Set the new password for the user
        self.user.set_password(new_password)
        self.user.save()
        return self.user


class SchoolDataSerializer(serializers.ModelSerializer):
    education_stage = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = SchoolDataModel
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classe
        # Add other fields as needed
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    # Include password field for writing only
    password = serializers.CharField(write_only=True)
    birth_date = serializers.DateField(

        format="%d/%m/%Y",
        input_formats=["%d/%m/%Y", "%d/%m/%Y"]
    )

    class Meta:
        model = Person
        fields = "__all__"  # Add other fields as needed

    def create(self, validated_data):
        # Pop password from validated data
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)  # Call superclass create method

        if password:
            # Set password using set_password method
            instance.set_password(password)
            instance.save()  # Save instance to ensure password is hashed
        return instance

    def update(self, instance, validated_data):
        # Pop password from validated data
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)  # Call superclass update method

        if password:
            # Set password using set_password method
            instance.set_password(password)
            instance.save()  # Save instance to ensure password is hashed
        return instance


# class SchoolMembersSerializer(serializers.ModelSerializer):
#     person = PersonSerializer()
#     profile_image = Base64ImageField(
#         max_length=None, use_url=True,
#     )
#     class Meta:
#         model = SchoolMembers
#         # Add other fields as needed
#         fields = "__all__"
#         extra_kwargs = {'school': {'required': False},'profile_image': {'required': False}}


#     def create(self, validated_data):
#         person_data = validated_data.pop('person')
#         email_ = person_data["email"]
#         person_serializer = PersonSerializer(data=person_data, context=self.context)  # Pass context
#         if person_serializer.is_valid():
#             if Person.objects.filter(email=email_).exists() == False:
#                 person = person_serializer.save()
#                 school_member = SchoolMembers.objects.create(person=person, **validated_data)
#                 return school_member
#             else:
#                 raise serializers.ValidationError("Person data is alredy Exists")


#         else:
#             # Handle serializer errors if needed
#             raise serializers.ValidationError("Person data is not valid")


class SchoolMembersSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    profile_image = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = SchoolMembers
        fields = '__all__'
        extra_kwargs = {'school': {'required': False},
                        'profile_image': {'required': False},
                         'device_token': {'required': False}, 
                        }

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        email_ = person_data.get('email')

        # Check if a person with the same email already exists
        try:
            person = Person.objects.get(email=email_)
        except Person.DoesNotExist:
            person_serializer = PersonSerializer(
                data=person_data, context=self.context)
            if person_serializer.is_valid():
                person = person_serializer.save()
            else:
                raise serializers.ValidationError("Person data is not valid")
        else:
            # Update existing person with new data
            person_serializer = PersonSerializer(
                instance=person, data=person_data, partial=True, context=self.context)
            if person_serializer.is_valid():
                person = person_serializer.save()
            else:
                raise serializers.ValidationError("Person data is not valid")

        validated_data['person'] = person
        return super().create(validated_data)

    def update(self, instance, validated_data):
        person_data = validated_data.pop('person')
        person_serializer = PersonSerializer(
            instance=instance.person, data=person_data, partial=True, context=self.context)
        if person_serializer.is_valid():
            person = person_serializer.save()
            validated_data['person'] = person
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError("Person data is not valid")


class ParentLightSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.person.first_name')
    last_name = serializers.CharField(source='user.person.last_name')
    phone_number = serializers.CharField(source='user.person.phone')
    gender = serializers.CharField(source='user.person.gender')
    email = serializers.EmailField(source='user.person.email')
    device_token = serializers.CharField(source='user.device_token')
    profile_image = serializers.CharField(source='user.profile_image')
    user_id = serializers.IntegerField(source='user.id')
    person_id = serializers.IntegerField(source='user.person.id')

    class Meta:
        model = Parent
        fields = [
            'id', 'user_id', 'person_id', 'first_name', 'last_name', 
            'phone_number', 'gender', 'email', 'device_token','profile_image'
        ]
        
        
class StudentLightSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.person.first_name')
    last_name = serializers.CharField(source='user.person.last_name')
    phone_number = serializers.CharField(source='user.person.phone')
    gender = serializers.CharField(source='user.person.gender')
    email = serializers.EmailField(source='user.person.email')
    device_token = serializers.CharField(source='user.device_token')
    profile_image = serializers.CharField(source='user.profile_image')
    user_id = serializers.IntegerField(source='user.id')
    person_id = serializers.IntegerField(source='user.person.id')

    class Meta:
        model = Student
        fields = [
            'id', 'user_id', 'person_id', 'first_name', 'last_name', 
            'phone_number', 'gender', 'email', 'device_token','profile_image'
        ]
        
    

class TeacherLightSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.person.first_name')
    last_name = serializers.CharField(source='user.person.last_name')
    phone_number = serializers.CharField(source='user.person.phone')
    gender = serializers.CharField(source='user.person.gender')
    email = serializers.EmailField(source='user.person.email')
    device_token = serializers.CharField(source='user.device_token')
    profile_image = serializers.CharField(source='user.profile_image')
    user_id = serializers.IntegerField(source='user.id')
    person_id = serializers.IntegerField(source='user.person.id')

    class Meta:
        model = Teacher
        fields = [
            'id', 'user_id', 'person_id', 'first_name', 'last_name', 
            'phone_number', 'gender', 'email', 'device_token','profile_image'
        ]


class ParentSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer()

    class Meta:
        model = Parent
        fields = "__all__"
        extra_kwargs = {'student': {'required': False}, }

    def create(self, validated_data):
        person_data = validated_data.pop("user")
        person_data["school"] = person_data["school"].id

        member_serializer = SchoolMembersSerializer(
            data=person_data, context=self.context
        )  # Pass context
        if member_serializer.is_valid():
            person = member_serializer.save()  # Use save() to create the person object
            parent = Parent.objects.create(user=person, **validated_data)

            return parent
        else:
            # Handle serializer errors if needed
            raise serializers.ValidationError(
                f"Memeber data is not valid {member_serializer.errors}")

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user_data["school"] = user_data["school"].id

        member_serializer = SchoolMembersSerializer(
            instance=instance.user, data=user_data, partial=True, context=self.context
        )
        if member_serializer.is_valid():
            person = member_serializer.save()
            validated_data["user"] = person
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError(
                {"error": member_serializer.errors})


class TeacherSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer()

    class Meta:
        model = Teacher
        fields = ("id", "user", "qualification", "experience", "specialization",
                  "address", "joining_date")  # Add other fields as needed

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user_data["school"] = user_data["school"].id

        member_serializer = SchoolMembersSerializer(
            instance=instance.user, data=user_data, partial=True, context=self.context
        )
        if member_serializer.is_valid():
            person = member_serializer.save()
            validated_data["user"] = person
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError(
                {"error": member_serializer.errors})

    def create(self, validated_data):
        person_data = validated_data.pop("user")
        person_data["school"] = person_data["school"].id

        member_serializer = SchoolMembersSerializer(
            data=person_data, context=self.context
        )  # Pass context
        if member_serializer.is_valid():
            person = member_serializer.save()  # Use save() to create the person object
            teacher = Teacher.objects.create(user=person, **validated_data)
            return teacher
        else:
            # Handle serializer errors if needed
            raise serializers.ValidationError(
                f"Memeber data is not valid {member_serializer.errors}"
            )


class StudentSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer()
    classe_id = serializers.PrimaryKeyRelatedField(
        queryset=Classe.objects.all(), source='classe', write_only=True)
    
      # Handle null monthly_payment
    
    class Meta:
        model = Student
        fields = ("id", "user", "classe_id" )  # Add other fields as needed

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['classe'] = ClassSerializer(instance.classe).data
        
         # Include parents only if they are available
        monthly_payment = MonthlyPayment.objects.filter(student=instance.id)
        
        representation['monthly_payment'] = MonthlyPaymentSerializer(monthly_payment,read_only=True, many=True,allow_null=True).data
        
            
        parents = instance.parents.all()
        if parents.exists():
            representation['parents'] = ParentLightSerializer(parents, many=True).data
        else:
            representation['parents'] = None
            
        return representation

    def create(self, validated_data):
        person_data = validated_data.pop('user')
        person_data['school'] = person_data['school'].id

        member_serializer = SchoolMembersSerializer(
            data=person_data, context=self.context)

        if member_serializer.is_valid():
            person = member_serializer.save()   # Use save() to create the person object
            student = Student.objects.create(user=person, **validated_data)

            return student

        else:
            # Handle serializer errors if needed
            raise serializers.ValidationError(
                f"Memeber data is not valid {member_serializer.errors}")

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_data['school'] = user_data['school'].id

        member_serializer = SchoolMembersSerializer(
            instance=instance.user, data=user_data, partial=True, context=self.context)
        if member_serializer.is_valid():
            person = member_serializer.save()
            validated_data['user'] = person
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError(
                {"error": member_serializer.errors})


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "subject_name", "school"]


class ProfileParentSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer(read_only=True)
    student = StudentSerializer(read_only=True, many=True)

    class Meta:
        model = Parent
        fields = "__all__"
        extra_kwargs = {'student': {'required': False}, }
# Add other fields as needed


class ClassRoomSerializer(serializers.ModelSerializer):

    subjects_taught_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), source="subjects_taught", write_only=True)
    assigned_teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source="assigned_teacher", write_only=True)
    classes_taught_id = serializers.PrimaryKeyRelatedField(
        queryset=Classe.objects.all(), source="classes_taught", write_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["classes_taught"] = ClassSerializer(
            instance.classes_taught).data
        representation["subjects_taught"] = SubjectSerializer(
            instance.subjects_taught).data
        representation["assigned_teacher"] = TeacherSerializer(
            instance.assigned_teacher).data
        return representation

    class Meta:
        model = ClassRoom
        fields = [
            "id",
            "room_name",
            "capacity",
            "building",
            "is_virtual",
            "school",
            "classes_taught_id",
            "assigned_teacher_id",
            "subjects_taught_id",
        ]  # Add other fields as needed
        extra_kwargs = {
            "classes_taught": {"required": True},
            "assigned_teacher": {"required": True},
            "subjects_taught": {"required": True},
            "school": {"required": True},
        }


class ScheduleClassSerializer(serializers.ModelSerializer):
    # Write-only field to accept only the ID in POST requests
    class_room_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassRoom.objects.all(),
        source='class_room',
        write_only=True
    )

    start_time = serializers.TimeField(format="%H:%M")
    end_time = serializers.TimeField(format="%H:%M")

    def to_representation(self, instance):
        # Call super correctly for a ModelSerializer
        representation = super().to_representation(instance)
        # Add the nested class_room details using ClassRoomSerializer
        representation['class_room'] = ClassRoomSerializer(
            instance.class_room).data
        return representation

    class Meta:
        model = ClassSchedule
        fields = ("class_room_id", "start_time",
                  "school", "end_time", "day", "id")


 
class ClassScheduleSerializer(serializers.ModelSerializer):
    class_room = ClassRoomSerializer()
    start_time = serializers.TimeField(format="%H:%M")
    end_time = serializers.TimeField(format="%H:%M")
    class Meta:
        model = ClassSchedule
        fields = ['id', 'day', 'start_time', 'end_time', 'class_room', 'school']

    def validate(self, data):
        # Manually call the model's clean method to perform validation
        try:
            instance = ClassSchedule(**data)
            instance.clean()  # Run the model's validation logic
        except ValidationError as e:
            raise serializers.ValidationError(e.message)  # Convert ValidationError to DRF ValidationError

        return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user_id"] = self.user.id
        data["is_staff"] = self.user.is_staff
        data["is_teacher"] = self.user.is_teacher
        data["is_owner"] = self.user.is_owner
        data["is_student"] = self.user.is_student

        ismember = SchoolMembers.objects.filter(
            person_id=self.user.id).exists()
        if (ismember):
            member = SchoolMembers.objects.get(person_id=self.user.id)
            serializers = SchoolMembersSerializer(instance=member)
            data["data"] = serializers.data

        return data


class EventsSerializer(serializers.ModelSerializer):
    date_start = serializers.DateTimeField(
        required=False,
        input_formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"],
    )
    date_end = serializers.DateTimeField(
        required=False,
        input_formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"],
    )

    class Meta:
        model = Events
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassSchedule.objects.all(), source="schedule", write_only=True
    )

    class Meta:
        model = Attendance
        fields = ("id", "student", "school", "schedule_id", "date", "teacher")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["schedule"] = ScheduleClassSerializer(
            instance.schedule).data
        return representation


# class StatisticSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Attendance
#         fie


class NotificationSerializer(serializers.ModelSerializer):
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=SchoolMembers.objects.all(), source="sender", write_only=True
    )

    class Meta:
        model = Notification
        fields = ("id", "message", "role", "sender_id",
                  "status", "author", "timestamp")

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation["sender"] = SchoolMembersSerializer(
            instance.sender).data
        return representation


class StaffSerialization(serializers.ModelSerializer):
    user = SchoolMembersSerializer()

    class Meta:
        model = Staff
        fields = "__all__"

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user_data["school"] = user_data["school"].id

        member_serializer = SchoolMembersSerializer(
            instance=instance.user, data=user_data, partial=True, context=self.context
        )
        if member_serializer.is_valid():
            person = member_serializer.save()
            validated_data["user"] = person
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError(
                {"error": member_serializer.errors})

    def create(self, validated_data):
        person_data = validated_data.pop("user")
        person_data["school"] = person_data["school"].id

        member_serializer = SchoolMembersSerializer(
            data=person_data, context=self.context
        )

        if member_serializer.is_valid():
            person = member_serializer.save()  # Use save() to create the person object
            staff = Staff.objects.create(user=person, **validated_data)

            return staff

        else:
            # Handle serializer errors if needed
            raise serializers.ValidationError(
                f"Memeber data is not valid {member_serializer.errors}"
            )


class ResultSerializers(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source="student", write_only=True
    )
    exam_id = serializers.PrimaryKeyRelatedField(
        queryset=Exam.objects.all(), source="exam", write_only=True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["student"] = StudentSerializer(instance.student).data
        representation["exam"] = ExamSerializers(instance.exam).data
        return representation

    class Meta:
        model = Result
        fields = "__all__"


class ExamSerializers(serializers.ModelSerializer):
    classe_id = serializers.PrimaryKeyRelatedField(
        queryset=Classe.objects.all(), source="class_association", write_only=True
    )

    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), source="subject_association", write_only=True
    )

    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source="teacher", write_only=True
    )

    class Meta:
        model = Exam
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["class_association"] = ClassSerializer(
            instance.class_association
        ).data
        representation["subject_association"] = SubjectSerializer(
            instance.subject_association
        ).data
        representation["teacher"] = TeacherSerializer(instance.teacher).data
        return representation


class HomeworkSerializer(serializers.ModelSerializer):
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source="assigned_by", write_only=True, required=False
    )
    classe_id = serializers.PrimaryKeyRelatedField(
        queryset=Classe.objects.all(), source="assigned_class", write_only=True, required=False
    )

    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), source="subject", write_only=True, required=False
    )

    class Meta:
        model = Homework
        fields = '__all__'

    def validate(self, data):
        # Make sure either teacher_id or assigned_by is set
        if not data.get('assigned_by') and not data.get('teacher_id'):
            raise serializers.ValidationError(
                {"assigned_by": "This field is required."})

        # Make sure either subject_id or subject is set
        if not data.get('subject') and not data.get('subject_id'):
            raise serializers.ValidationError(
                {"subject": "This field is required."})
            
        if not data.get('assigned_class') and not data.get('classe_id'):
            raise serializers.ValidationError(
                {"assigned_class": "This field is required."})

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Check if the assigned_by (teacher) exists before serializing
        representation["assigned_by"] = TeacherSerializer(
            instance.assigned_by).data
        representation["subject"] = SubjectSerializer(instance.subject).data
        representation["assigned_class"] = ClassSerializer(instance.assigned_class).data

        return representation

     


class PerformanceSerializer(serializers.ModelSerializer):
    performance = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "performance"]

    def get_performance(self, obj):
        return calculate_monthly_performance(obj)


class AttendancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "date", "student"]



class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ('user', 'token')
        
class PubSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubModel
        fields = "__all__"
        

 


