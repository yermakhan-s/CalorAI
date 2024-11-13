from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import MyUser
from django.conf import settings
import requests


class SendMessageToUsersView(APIView):
    """
    API endpoint to send a message to specific users or all users via Telegram bot.
    """

    def post(self, request, *args, **kwargs):
        try:
            # Parse the request body
            message = request.data.get("message", "")
            user_ids = request.data.get("user_ids", [])  # Optional list of user IDs

            # Validate message
            if not message:
                return Response({"error": "Message cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch users
            if user_ids:
                users = MyUser.objects.filter(user_id__in=user_ids)
            else:
                users = MyUser.objects.all()

            # Send message to each user
            results = []
            for user in users:
                if user.user_id:  # Ensure user_id exists
                    telegram_response = self.send_telegram_message(user.user_id, message)
                    results.append({
                        "user_id": user.user_id,
                        "username": user.username,
                        "status": "sent" if telegram_response else "failed"
                    })

            return Response({"results": results}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def send_telegram_message(chat_id, message):
        """
        Send a message to a Telegram user.
        """
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return True
            else:
                print(f"Failed to send message to {chat_id}: {response.text}")
                return False
        except Exception as e:
            print(f"Error sending message to {chat_id}: {str(e)}")
            return False
