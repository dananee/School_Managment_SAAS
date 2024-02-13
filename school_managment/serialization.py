from rest_framework import serializers
from .models import ClassSchedule, SchoolDataModel,  Genders, Class, SchoolMembers, Teacher, Subject, ClassRoom,Person
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SchoolDataSerializer(serializers.ModelSerializer):
    education_stage = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = SchoolDataModel
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        # Add other fields as needed
        fields = ['class_id', 'class_name', 'school']
        
class PersonSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # We'll handle password separately

    class Meta:
        model = Person
        fields = "__all__"
        extra_kwargs = {
            'profile_image': {'required': False},  # Allow profile image to be optional
        }

    def create(self, validated_data):
        # Create and return a new 'Person' instance
        return Person.objects.create_user(**validated_data)
         

class SchoolMembersSerializer(serializers.ModelSerializer):
    person  = PersonSerializer()
    
    class Meta:
        model = SchoolMembers
        # Add other fields as needed
        fields = '__all__'
    
    # def create(self, validated_data):
    #     user_data = validated_data.pop('person')
        
    #     person_profile = PersonSerializer.create(PersonSerializer(), validated_data=user_data)
    #     person, created = User.objects.update_or_create(person=person_profile)
    #     return person

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


class ScheduleClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = '__all__'  # Add other fields as needed


class ClassRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassRoom
        fields = ['room_id', 'room_name', 'capacity', 'building', 'is_virtual',
                  'classes_taught', 'assigned_teacher', 'subjects_taught']  # Add other fields as needed
        extra_kwargs = {'classes_taught': {'required': True}, 'assigned_teacher': {
            'required': True}, 'subjects_taught': {'required': True}, }
        





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
    

