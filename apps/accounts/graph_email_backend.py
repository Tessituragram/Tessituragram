import msal
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

DEFAULT_MAILBOX = "verify_email@tessituragram.com"


class GraphEmailBackend(BaseEmailBackend):
    def get_access_token(self):
        authority = f"https://login.microsoftonline.com/{settings.MS_TENANT_ID}"
        app = msal.ConfidentialClientApplication(
            settings.MS_CLIENT_ID, authority=authority, client_credential=settings.MS_CLIENT_SECRET
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in result:
            raise Exception(f"Failed to get token: {result.get('error_description')}")
        return result["access_token"]

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        token = self.get_access_token()
        sent_count = 0

        for message in email_messages:
            sender = message.from_email or DEFAULT_MAILBOX
            url = f"https://graph.microsoft.com/v1.0/users/{sender}/sendMail"

            payload = {
                "message": {
                    "subject": message.subject,
                    "body": {"contentType": "Text", "content": message.body},
                    "toRecipients": [{"emailAddress": {"address": addr}} for addr in message.to],
                }
            }

            if hasattr(message, "reply_to") and message.reply_to:
                payload["message"]["replyTo"] = [
                    {"emailAddress": {"address": addr}} for addr in message.reply_to
                ]

            response = requests.post(
                url,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json=payload,
            )
            if response.status_code == 202:
                sent_count += 1
            elif not self.fail_silently:
                response.raise_for_status()

        return sent_count