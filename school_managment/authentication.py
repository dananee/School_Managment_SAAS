# authentication.py
from django.contrib.auth.backends import BaseBackend
from .models import Person

class PersonAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        print(f"Email : {email} ")
        try:
            person = Person.objects.get(email=email)
            if person.check_password(password):
                return person
        except Person.DoesNotExist:
            print(f"Email : {email} DoesNotExist")
            return None

    def get_user(self, user_id):
        try:
            return Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            print(f"User Id : {user_id} DoesNotExist")
            return None
