from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from .models import SchoolMembers,Student,Parent,Classe
import json
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import requests
from school_managment_saas.settings import FCM_CREDENTIALS



# Define FCM project settings
FCM_URL = 'https://fcm.googleapis.com/v1/projects/edugenius-efee7/messages:send'

# Load credentials
credentials = Credentials.from_service_account_file(
    FCM_CREDENTIALS,
    scopes=["https://www.googleapis.com/auth/firebase.messaging"]
)

def send_fcm_notification(device_token, title, body):
   
    # Prepare the notification payload
    message = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": body
            },
            "apns": {  # Optional: Add iOS-specific fields
                "payload": {
                    "aps": {
                        "sound": "default"
                    }
                }
            },
            "android": {  # Optional: Add Android-specific fields
                "priority": "HIGH"
            }
        }
    }

    # Generate access token
    credentials.refresh(Request())
    access_token = credentials.token

    # Make the HTTP request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.post(FCM_URL, headers=headers, data=json.dumps(message))

    if response.status_code != 200:
        raise Exception(f"FCM error: {response.content.decode()}")

    return response.json()


def send_notification(user_id, title, message):
    """
    Send a notification to a specific user.

    Args:
        user_id (int): ID of the SchoolMember recipient.
        title (str): Notification title.
        message (str): Notification message.

    Returns:
        Notification: The created notification instance.
    """
    try:
        recipient = SchoolMembers.objects.get(pk=user_id)

        # Send FCM Notification
        if recipient.device_token:
            send_fcm_notification(recipient.device_token, title, message)
        else:
            raise ValueError("User does not have a valid device token.")

        
    except SchoolMembers.DoesNotExist:
        raise ValueError("User with the given ID does not exist.")
    

def send_bulk_notifications(user_ids, title, message):
    """
    Send notifications to multiple users.

    Args:
        user_ids (list[int]): List of SchoolMember IDs.
        title (str): Notification title.
        message (str): Notification body.

    Returns:
        dict: Summary of success and failures.
    """
    successful = []
    failed = []

    for user_id in user_ids:
        try:
            recipient = SchoolMembers.objects.get(pk=user_id)

            # Send FCM Notification
            if recipient.device_token:
                send_fcm_notification(recipient.device_token, title, message)
                successful.append(user_id)
            else:
                failed.append({"user_id": user_id, "error": "No valid device token."})

        except SchoolMembers.DoesNotExist:
            failed.append({"user_id": user_id, "error": "User does not exist."})
        except Exception as e:
            failed.append({"user_id": user_id, "error": str(e)})

    return {
        "successful": successful,
        "failed": failed
    }


def send_bulk_class_notifications(class_ids, title, message):
    successful = []
    failed = []

    for class_id in class_ids:
        try:
            # Get all students in the class
            students = Student.objects.filter(classe__id=class_id)

            # Send notification to students
            for student in students:
                if student.user.device_token:
                    send_fcm_notification(student.user.device_token, title, message)
                    successful.append({"class_id": class_id, "student_id": student.id})
                else:
                    failed.append({"class_id": class_id, "student_id": student.id, "error": "No valid device token for student."})

            # Get all parents of students in the class
            parents = Parent.objects.filter(student__in=students)

            # Send notification to parents
            for parent in parents:
                if parent.user.device_token:
                    send_fcm_notification(parent.user.device_token, title, message)
                    successful.append({"class_id": class_id, "parent_id": parent.id})
                else:
                    failed.append({"class_id": class_id, "parent_id": parent.id, "error": "No valid device token for parent."})

        except Classe.DoesNotExist:
            failed.append({"class_id": class_id, "error": "Classe does not exist."})
        except Exception as e:
            failed.append({"class_id": class_id, "error": str(e)})

    return {
        "successful": successful,
        "failed": failed,
    }
