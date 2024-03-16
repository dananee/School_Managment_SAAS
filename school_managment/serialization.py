import json
from rest_framework import serializers
from .models import Attendance, ClassSchedule, Events, NotificationModel, Parent, SchoolDataModel,  Genders, Classe, SchoolMembers, Student, Teacher, Subject, ClassRoom, Person
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
        model = Classe
        # Add other fields as needed
        fields = "__all__"

    


class PersonSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Include password field for writing only

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


class TeacherSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer()
     

    class Meta:
        model = Teacher
        fields = "__all__"  # Add other fields as needed
        extra_kwargs = {'teaching_classes': {'required': True}}
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_data['school'] = user_data['school'].id
        print(f"USer {user_data}")
        member_serializer = SchoolMembersSerializer(instance=instance.user, data=user_data, partial=True, context=self.context)
        if member_serializer.is_valid():
            person = member_serializer.save()
            validated_data['user'] = person
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError({"error":member_serializer.errors})

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
    classe_id = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(),source='classe',write_only=True)

    class Meta:
        model = Student
        fields =  ("id","user", "classe_id") # Add other fields as needed
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['classe'] = ClassSerializer(instance.classe).data
        return representation
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_data['school'] = user_data['school'].id
        print(f"USer {user_data}")
        member_serializer = SchoolMembersSerializer(instance=instance.user, data=user_data, partial=True, context=self.context)
        if member_serializer.is_valid():
            person = member_serializer.save()
            validated_data['user'] = person
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError({"error":member_serializer.errors})


    def create(self, validated_data):
        person_data = validated_data.pop('user')
        person_data['school'] = person_data['school'].id
        
        
        member_serializer = SchoolMembersSerializer(data=person_data, context=self.context)
        
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
        fields = ['id', 'subject_name']


  # Add other fields as needed


class ClassRoomSerializer(serializers.ModelSerializer):
    classes_taught = ClassSerializer(many=True,read_only=True)
    subjects_taught = SubjectSerializer( read_only=True)
    assigned_teacher = TeacherSerializer(read_only=True)
    class Meta:
        model = ClassRoom
        fields = ['id', 'room_name', 'capacity', 'building', 'is_virtual','school',
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

# class StatisticSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Attendance
#         fie


class ParentSerializer(serializers.ModelSerializer):
    user = SchoolMembersSerializer()

    class Meta:
        model = Parent
        fields = "__all__"



class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationModel
        fields = "__all__"