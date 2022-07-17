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


def notify_user_gig(properties, user, user_email_address, list_user_email):
    """
    Sends email to user to notify them a match has been found
    and a gig has been automatically created.
    """
    destination = user_email_address

    email_msg = f"""
Congratulations!!

We found you a gig... clever Late Gigs!

Gig Details:
{properties[0].title()} will play a(n) {properties[3].title()} set
 at {properties[1].title()} venue
this coming {properties[2].title()}
for a fee of €{properties[4]}

Gig initiated by the: {user}

We strongly recommend you now contact your match via email:
{list_user_email}

Late Gigs accepts no responsibility for gigs
that are created automatically but not honoured.

Thank you for using Late Gigs!
For support and more information contact us via lategigs@davidcalikes.com
"""

    mime_message = MIMEMultipart()
    mime_message['to'] = f'{destination}'
    mime_message['subject'] = "Late Gigs! Booking Confirmed!"
    mime_message.attach(MIMEText(email_msg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    service_gmail = build("gmail", "v1", credentials=credentials)
    # pylint: disable=E1101
    service_gmail.users().messages().send(userId='me', body={'raw':
                                          raw_string}).execute()

    notify_list_user_gig(properties, user, user_email_address, list_user_email)


def notify_list_user_gig(properties, user, user_email_address,
                         list_user_email):
    """
    Sends email to user to notify them a match has been found
    and a gig has been automatically created.
    """
    destination = list_user_email

    email_msg = f"""
Congratulations!!

We found you a gig... clever Late Gigs!

Gig Details:
{properties[0].title()} will play a(n) {properties[3].title()} set
 at {properties[1].title()} venue
this coming {properties[2].title()}
for a fee of €{properties[4]}

Gig initiated by the: {user}

We strongly recommend you now contact your match via email:
{user_email_address}

Late Gigs accepts no responsibility for gigs that are created automatically
but not honoured.

Thank you for using Late Gigs!
For support and more information contact us via lategigs@davidcalikes.com
"""

    mime_message = MIMEMultipart()
    mime_message['to'] = f'{destination}'
    mime_message['subject'] = "Late Gigs! Booking Confirmed!"
    mime_message.attach(MIMEText(email_msg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    service_gmail = build("gmail", "v1", credentials=credentials)
    # pylint: disable=E1101
    service_gmail.users().messages().send(userId='me', body={'raw':
                                          raw_string}).execute()
    print("Success! Gig confirmed!")
    print(f"""
The Details:
{properties[0]} wil play a {properties[3]} set
 at {properties[1]} venue
this coming {properties[2]}
for a fee of €{properties[4]}
Gig user is: {user}
""")
    print("Thank you for Using Late Gigs!")
    print("Check your email for booking confirmation!")
    print("Please check spam folder if you do not recieve an email")
    print("within the next few minutes")
    exit()


def email_verify(name, user, user_email_address, user_pin):
    """
    Sends email to user with unique PIN number for Email Account Verification
    """
    destination = user_email_address

    email_msg = f"""
Thank you for registering with Late Gigs.

Here are your details:
{user.title()}: {name}

We really hope we can create a gig for you!

Your unique pin number is {user_pin}
Return to Late Gigs app to complete your search

This email is automated...

"""

    mime_message = MIMEMultipart()
    mime_message['to'] = f'{destination}'
    mime_message['subject'] = "Welcome to Late Gigs!"
    mime_message.attach(MIMEText(email_msg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    service_gmail = build("gmail", "v1", credentials=credentials)
    # pylint: disable=E1101
    service_gmail.users().messages().send(userId='me', body={'raw':
                                          raw_string}).execute()
