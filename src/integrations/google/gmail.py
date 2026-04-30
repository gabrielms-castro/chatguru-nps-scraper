import base64
import logging
import os.path
import re
import time

from urllib.parse import urlparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def wait_for_emails(service, sender, expected_count, after_timestamp, timeout=300, interval=15):
    deadline = time.time() + timeout
    messages = []

    while time.time() < deadline:

        results = service.users().messages().list(
            userId='me',
            q=f'from:{sender} after:{after_timestamp}'
        ).execute()

        messages = results.get('messages', [])
        logging.info("Aguardando e-mails... (%s/%s)", len(messages), expected_count)
        
        if len(messages) >= expected_count:
            return messages
        
        time.sleep(interval)
        
    raise TimeoutError(f"Timeout: apenas {len(messages)}/{expected_count} e-mails recebidos de {sender}")


def get_email_messages(service, messages):

    download_links = []

    for message in messages:
        try:
            result = service.users().messages().get(userId='me', id=message['id']).execute()

            email_data = result.get("payload") \
                .get("parts")[0] \
                .get("body") \
                .get("data")

            body = base64.urlsafe_b64decode(email_data).decode()
            link = re.findall(r'https?://[^\s<>"\']+', body)[0]
            filename = urlparse(link).path.split("/")[-1]

            download_links.append({"filename": filename, "link": link})

        except (HttpError, IndexError, AttributeError) as exc:
            logging.exception("Erro ao processar e-mail %s: %s", message['id'], exc)

    return download_links
