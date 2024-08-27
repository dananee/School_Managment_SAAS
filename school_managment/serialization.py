import json
from rest_framework import serializers
from .models import (
    Attendance,
    ClassSchedule,
    Events,
    Exam,
    FCMDevice,
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
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import (
    PasswordResetConfirmSerializer as DjoserPasswordResetConfirmSerializer,
)

from phonenumber_field.serializerfields import PhoneNumberField



def calculate_performance(student):
    results = Result.objects.filter(student=student)
    total_score = sum(result.score for result in results)
    average_score = total_score / len(results) if len(results) > 0 else 0
    return average_score


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
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
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


class CustomPasswordResetConfirmSerializer(DjoserPasswordResetConfirmSerializer):
    def validate_uid(self, uid):
        try:
            user = Person.objects.get(id=uid)
        except Person.DoesNotExist:
            raise serializers.ValidationError("Invalid email address")
        return user


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
    password = serializers.CharField(write_only=True)  # Include password field for writing only
    birth_date = serializers.DateField(
        
        format="%d/%m/%Y", 
        input_formats=["%d/%m/%Y", "%d/%m/%Y"]
    )

    
    class Meta:
        model = Person
        fields = "__all__"  # Add other fields as needed

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Pop password from validated data
        instance = super().create(validated_data)  # Call superclass create method

        if password:
            instance.set_password(password)  # Set password using set_password method
            instance.save()  # Save instance to ensure password is hashed
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  # Pop password from validated data
        instance = super().update(instance, validated_data)  # Call superclass update method

        if password:
            instance.set_password(password)  # Set password using set_password method
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
        extra_kwargs = {'school': {'required': False}, 'profile_image': {'required': False}}

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        email_ = person_data.get('email')

        # Check if a person with the same email already exists
        try:
            person = Person.objects.get(email=email_)
        except Person.DoesNotExist:
            person_serializer = PersonSerializer(data=person_data, context=self.context)
            if person_serializer.is_valid():
                person = person_serializer.save()
            else:
                raise serializers.ValidationError("Person data is not valid")
        else:
            # Update existing person with new data
            person_serializer = PersonSerializer(instance=person, data=person_data, partial=True, context=self.context)
            if person_serializer.is_valid():
                person = person_serializer.save()
            else:
                raise serializers.ValidationError("Person data is not valid")

        validated_data['person'] = person
        return super().create(validated_data)

    def update(self, instance, validated_data):
        person_data = validated_data.pop('person')
        person_serializer = PersonSerializer(instance=instance.person, data=person_data, partial=True, context=self.context)
        if person_serializer.is_valid():
            person = person_serializer.save()
            validated_data['person'] = person
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError("Person data is not valid")



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
            raise serializers.ValidationError({"error": member_serializer.errors})


class TeacherSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer()
    teaching_classes_id =  serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(), source="teaching_classes",many=True,write_only=True)

    class Meta:
        model = Teacher
        fields = ("id","user","qualification","teaching_classes_id","experience","specialization","address","joining_date")  # Add other fields as needed
       
       
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["teaching_classes"] = ClassSerializer(instance.teaching_classes,many=True).data
        return representation
    

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
            raise serializers.ValidationError({"error": member_serializer.errors})

    def create(self, validated_data):
        person_data = validated_data.pop("user")
        person_data["school"] = person_data["school"].id
        teaching_classes = validated_data.pop("teaching_classes")

 
        member_serializer = SchoolMembersSerializer(
            data=person_data, context=self.context
        )  # Pass context
        if member_serializer.is_valid():
            person = member_serializer.save()  # Use save() to create the person object
            teacher = Teacher.objects.create(user=person, **validated_data)
            teacher.teaching_classes.add(*teaching_classes)

            return teacher
        else:
            # Handle serializer errors if needed
            raise serializers.ValidationError(
                f"Memeber data is not valid {member_serializer.errors}"
            )


class StudentSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer()
    classe_id = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(),source='classe',write_only=True)

    class Meta:
        model = Student
        fields =  ("id","user", "classe_id") # Add other fields as needed
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['classe'] = ClassSerializer(instance.classe).data
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
       
        member_serializer = SchoolMembersSerializer(instance=instance.user, data=user_data, partial=True, context=self.context)
        if member_serializer.is_valid():
            person = member_serializer.save()
            validated_data['user'] = person
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError({"error":member_serializer.errors})


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "subject_name"]


# Add other fields as needed


class ClassRoomSerializer(serializers.ModelSerializer):
 
    subjects_taught_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), source="subjects_taught",write_only=True)
    assigned_teacher_id = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), source="assigned_teacher",write_only=True)
    classes_taught_id =  serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(), source="classes_taught",many=True,write_only=True)

     
       
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["classes_taught"] = ClassSerializer(instance.classes_taught,many=True).data
        representation["subjects_taught"] =  SubjectSerializer(instance.subjects_taught).data
        representation["assigned_teacher"] =  TeacherSerializer(instance.assigned_teacher).data
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
    class_room = ClassRoomSerializer()
    start_time = serializers.DateTimeField(format="%H:%M")
    end_time = serializers.DateTimeField(format="%H:%M")

    class Meta:
        model = ClassSchedule
        fields = "__all__"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user_id"] = self.user.id
        data["is_staff"] = self.user.is_staff
        data["is_owner"] = self.user.is_owner

        ismember = SchoolMembers.objects.filter(person_id=self.user.id).exists()
        if(ismember):
            member =  SchoolMembers.objects.get(person_id=self.user.id)
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
        representation["schedule"] = ScheduleClassSerializer(instance.schedule).data
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
        fields = ("id", "message", "role", "sender_id", "status", "author", "timestamp")

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation["sender"] = SchoolMembersSerializer(instance.sender).data
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
            raise serializers.ValidationError({"error": member_serializer.errors})

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


class AttendanceChartSerializers(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"


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


class PerformanceSerializer(serializers.ModelSerializer):
    performance = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "performance"]

    def get_performance(self, obj):
        return calculate_performance(obj)


class AttendancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "date", "student"]

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ('user', 'token')