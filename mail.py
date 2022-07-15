import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "creds.json"
credentials = service_account.Credentials.from_service_account_file(
    filename=SERVICE_ACCOUNT_FILE,
    scopes=["http://mail.google.com/"],
    subject="lategigs@davidcalikes.com"
)

emailMsg = """
           Welcome to Late Gigs! You're on the list!
           We'll be in touch as soon as we find you a
           match!
           """

mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'davidcalikes@gmail.com'
mimeMessage['subject'] = "Late Gigs! You're on the list!"
mimeMessage.attach(MIMEText(emailMsg, 'plain'))
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

service_gmail = build("gmail", "v1", credentials=credentials)
# pylint: disable=E1101
message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)
