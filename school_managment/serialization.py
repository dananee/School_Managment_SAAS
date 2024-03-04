import json
from rest_framework import serializers
from .models import Attendance, ClassSchedule, Events, SchoolDataModel,  Genders, Class, SchoolMembers, Student, Teacher, Subject, ClassRoom, Person
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import PasswordResetConfirmSerializer as DjoserPasswordResetConfirmSerializer

class Base64ImageField(serializers.ImageField):
     

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

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
        model = Class
        # Add other fields as needed
        fields = ['class_id', 'class_name', 'school','grade']

    


class PersonSerializer(serializers.ModelSerializer):
    # We'll handle password separately
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Person
        fields = "__all__"
         

    def create(self, validated_data):
        # Create and return a new 'Person' instance
        return Person.objects.create_user(**validated_data)


class SchoolMembersSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    profile_image = Base64ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model = SchoolMembers
        # Add other fields as needed
        fields = "__all__"
        extra_kwargs = {'school': {'required': False},'profile_image': {'required': False}}

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        person_serializer = PersonSerializer(data=person_data, context=self.context)  # Pass context
        if person_serializer.is_valid():
            person = person_serializer.save()  # Use save() to create the person object
            school_member = SchoolMembers.objects.create(person=person, **validated_data)
            return school_member
        else:
            # Handle serializer errors if needed
            raise serializers.ValidationError("Person data is not valid")



class TeacherSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer()
     

    class Meta:
        model = Teacher
        fields = "__all__"  # Add other fields as needed
        extra_kwargs = {'teaching_classes': {'required': True}}

    def create(self, validated_data):
        person_data = validated_data.pop('user')
        person_data['school'] = person_data['school'].id
        teaching_classes = validated_data.pop("teaching_classes")
         
        # print(f"TEACHER    {validated_data['teaching_classes'][0].class_id}")
        member_serializer = SchoolMembersSerializer(data=person_data, context=self.context)  # Pass context
        if member_serializer.is_valid():
            person = member_serializer.save()  # Use save() to create the person object
            teacher = Teacher.objects.create(user=person, **validated_data)
            teacher.teaching_classes.add(*teaching_classes)
              
            
            return teacher
        else:
            # Handle serializer errors if needed
            raise serializers.ValidationError(f"Memeber data is not valid {member_serializer.errors}")
        

class StudentSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer()
     

    class Meta:
        model = Student
        fields = "__all__"  # Add other fields as needed
        # extra_kwargs = {'teaching_classes': {'required': True}}

    def create(self, validated_data):
        person_data = validated_data.pop('user')
        person_data['school'] = person_data['school'].id
         
         
        # print(f"TEACHER    {validated_data['teaching_classes'][0].class_id}")
        member_serializer = SchoolMembersSerializer(data=person_data, context=self.context)  # Pass context
        if member_serializer.is_valid():
            person = member_serializer.save()   # Use save() to create the person object
            student = Student.objects.create(user=person, **validated_data)
             
            return student
        else:
            # Handle serializer errors if needed
            raise serializers.ValidationError(f"Memeber data is not valid {member_serializer.errors}")


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_id', 'subject_name']


  # Add other fields as needed


class ClassRoomSerializer(serializers.ModelSerializer):
    classes_taught = ClassSerializer(many=True,read_only=True)
    subjects_taught = SubjectSerializer( read_only=True)
    assigned_teacher = TeacherSerializer(read_only=True)
    class Meta:
        model = ClassRoom
        fields = ['room_id', 'room_name', 'capacity', 'building', 'is_virtual','school',
                  'classes_taught', 'assigned_teacher', 'subjects_taught']  # Add other fields as needed
        extra_kwargs = {'classes_taught': {'required': True}, 'assigned_teacher': {
            'required': True}, 'subjects_taught': {'required': True},'school': {'required': True} }


class ScheduleClassSerializer(serializers.ModelSerializer):
    class_room = ClassRoomSerializer()
    start_time = serializers.DateTimeField(format="%H:%M")
    end_time = serializers.DateTimeField(format="%H:%M")
    class Meta:
        model = ClassSchedule
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

     
   
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
      
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["is_staff"] = self.user.is_staff
        data["is_owner"] = self.user.is_owner


        
        return data


class EventsSerializer(serializers.ModelSerializer):
    date_start =serializers.DateTimeField(required=False,
                                          input_formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"])
    date_end =serializers.DateTimeField(required=False,
                                          input_formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"])
    class Meta:
        model = Events
        fields = "__all__"



class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"