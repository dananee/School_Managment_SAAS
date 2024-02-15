from rest_framework import serializers
from .models import ClassSchedule, SchoolDataModel,  Genders, Class, SchoolMembers, Teacher, Subject, ClassRoom, Person
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import PasswordResetConfirmSerializer as DjoserPasswordResetConfirmSerializer



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
        extra_kwargs = {
            # Allow profile image to be optional
            'profile_image': {'required': False},
        }

    def create(self, validated_data):
        # Create and return a new 'Person' instance
        return Person.objects.create_user(**validated_data)


class SchoolMembersSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = SchoolMembers
        # Add other fields as needed
        fields = '__all__'
        extra_kwargs = {'school': {'required': True}}

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
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'user', 'qualification', 'experience', 'specialization',
                  'contact_number', 'address', 'joining_date', 'teaching_classes']  # Add other fields as needed
        extra_kwargs = {'teaching_classes': {'required': True}}


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_id', 'subject_name']


  # Add other fields as needed


class ClassRoomSerializer(serializers.ModelSerializer):
    classes_taught = ClassSerializer(many=True,read_only=True)
    subjects_taught = SubjectSerializer(many=True,read_only=True)
    assigned_teacher = TeacherSerializer(read_only=True)
    class Meta:
        model = ClassRoom
        fields = ['room_id', 'room_name', 'capacity', 'building', 'is_virtual',
                  'classes_taught', 'assigned_teacher', 'subjects_taught']  # Add other fields as needed
        extra_kwargs = {'classes_taught': {'required': True}, 'assigned_teacher': {
            'required': True}, 'subjects_taught': {'required': True}, }


class ScheduleClassSerializer(serializers.ModelSerializer):
    class_room = ClassRoomSerializer()
    class Meta:
        model = ClassSchedule
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(f"*********************************** ")
        token = super().get_token(user)
        try:
            # Retrieve Person instance associated with the user
            person = Person.objects.get(id=user.id)
            # Include relevant information from the Person model in the token payload
            token['email'] = person.email
            token['first_name'] = person.first_name
            token['last_name'] = person.last_name
            # Add other user information as needed
        except Person.DoesNotExist:
            print("*********************************** ")
            pass
        return token
