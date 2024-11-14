# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from core.models import MyUser
# import requests
# import json

# def send_telegram_message(chat_id, message):
#     """
#     Send a message to a Telegram user.
#     """
#     url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
#     payload = {
#         "chat_id": chat_id,
#         "text": message
#     }

#     try:
#         response = requests.post(url, json=payload)
#         if response.status_code == 200:
#             return True
#         else:
#             print(f"Failed to send message to {chat_id}: {response.text}")
#             return False
#     except Exception as e:
#         print(f"Error sending message to {chat_id}: {str(e)}")
#         return False