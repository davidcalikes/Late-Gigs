import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = "creds.json"
credentials = service_account.Credentials.from_service_account_file(
    filename=SERVICE_ACCOUNT_FILE,
    scopes=["http://mail.google.com/"],
    subject="lategigs@davidcalikes.com"
)


def email_user():
    """
    Sends email to me because well, sure... I'm just great!
    """

    email_msg = """
               \nWelcome to Late Gigs! You're on the list!
               \n Hello Michelle from inside Davids latest app.
               \n This email is automated...
               ...clever David!!
               """

    mime_message = MIMEMultipart()
    mime_message['to'] = 'michellecalikes@gmail.com'
    mime_message['subject'] = "Late Gigs! You're on the list!"
    mime_message.attach(MIMEText(email_msg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    service_gmail = build("gmail", "v1", credentials=credentials)
    # pylint: disable=E1101
    message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)
    exit()
