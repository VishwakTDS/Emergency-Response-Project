# Setup details:
# Make sure to add SENDER_EMAIL, RECEIVER_EMAIL, and SENDER_PASSWORD to your .env file
# To get the SENDER_PASSWORD *DO NOT* use your email password
# Instead, go to the link: https://myaccount.google.com/apppasswords
# From there, sign in with your gmail account to generate an "App Password"

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config import sender_email, receiver_email, sender_password
 
def send_email(subject, body, img):
    msg = MIMEMultipart()

    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    filename = os.path.basename(img)
    attachment = open(img, "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())

    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, sender_password)
    text = msg.as_string()
    s.sendmail(sender_email, receiver_email, text)
    s.quit()