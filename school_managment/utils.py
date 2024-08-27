from firebase_admin import messaging


from school_managment.models import FCMDevice
  


# def send_fcm_notification(user, title, body, data=None):
#     devices = FCMDevice.objects.filter(user=user)
#     tokens = [device.token for device in devices]

#     message = messaging.MulticastMessage(
#         notification=messaging.Notification(
#             title=title,
#             body=body,
#         ),
#         data=data,
#         tokens=tokens,
#     )  

#     response = messaging.send_multicast(message)
#     return response

