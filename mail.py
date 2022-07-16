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


def email_user(properties, user, user_email_address):
    """
    Sends email to me because well, sure... I'm just great!
    """
    destination = user_email_address

    email_msg = f"""
                Welcome to Late Gigs! You're on the list!
                Hello David from inside LateGigs app.
                here are your details:
                {properties}
                we really hope we find your {user} a gig
                This email is automated...
                ...clever David!!
                """

    mime_message = MIMEMultipart()
    mime_message['to'] = f'{destination}'
    mime_message['subject'] = "Late Gigs! You're on the list!"
    mime_message.attach(MIMEText(email_msg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    service_gmail = build("gmail", "v1", credentials=credentials)
    # pylint: disable=E1101
    message = service_gmail.users().messages().send(userId='me', body={'raw':
                                                    raw_string}).execute()
    print(message)
    exit()


def email_verify(name, user, user_email_address, user_pin):
    """
    Sends email to user with unique PIN number for Email Account Verification
    """
    destination = user_email_address

    email_msg = f"""
                Welcome to Late Gigs!

                Hello  from inside LateGigs app.
                Here are your details:
                {user.title()}: {name}
                We really hope we can find create a gig for your {user}
                Your unique pin number is {user_pin}
                This email is automated...
                ...clever David!!
                """

    mime_message = MIMEMultipart()
    mime_message['to'] = f'{destination}'
    mime_message['subject'] = "Late Gigs! You're on the list!"
    mime_message.attach(MIMEText(email_msg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    service_gmail = build("gmail", "v1", credentials=credentials)
    # pylint: disable=E1101
    message = service_gmail.users().messages().send(userId='me', body={'raw':
                                                    raw_string}).execute()
    print(message)
