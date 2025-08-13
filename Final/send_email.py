import os
import json
import string
import smtplib
import mimetypes
import tempfile

from config import sender_email, sender_password, smtp_config

from email.message import EmailMessage
from email import encoders
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from sql_connection import get_agency_contact

def create_pdf(report_data, reportname):
    doc = SimpleDocTemplate(reportname, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    title_style = styles["Heading1"]
    elements.append(Paragraph("INCIDENT RESPONSE", title_style))
    elements.append(Spacer(1, 20))

    for key, value in report_data.items():
        key_space = key.replace('_', ' ')
        key_title = key_space.title()

        if isinstance(value, dict):
            value_str = json.dumps(value, indent=2)
        else:
            value_str = str(value)

        key_paragraph = Paragraph(f"<b>{key_title}:</b>", styles["Normal"])
        elements.append(key_paragraph)

        value_paragraph = Paragraph(value_str.replace("\n", "<br/>"), styles["Normal"])
        elements.append(value_paragraph)
        elements.append(Spacer(1, 10))

    doc.build(elements)

def send_email_mailhog(payload, img, agencies, location):

    contact_details = {val:"internationalagency@emergency.com" for val in agencies}

    location_details = location.split(',')
    country_location = location_details[-1].strip()
    state_location = location_details[-2].strip()

    if country_location.lower() == 'us':
        contact_details = get_agency_contact(agencies, state_location)

    state_location = location_details[-2].strip()
    # print(state_location)

    for responder in payload:
        msg = EmailMessage()

        recipient_data = "\n".join([f"{key}: {value}" for key, value in responder.items()])

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            pdf_report_path = temp_pdf.name
        
        # pdf_report = create_pdf(responder, pdf_report_path)
        create_pdf(responder, pdf_report_path)

        print(f"\nTHREAT TYPE: {responder["common_info"]["threat_type"]}")

        email_subject = f"Alert from ARES - {responder["common_info"]["threat_type"]}"
        email_body = recipient_data

        msg["Subject"] = email_subject
        msg["From"] = smtp_config["smtp_user"]
        msg["To"] = contact_details[responder["agency"]]
        msg.set_content(email_body)

        # Attach pdf report
        with open(pdf_report_path, "rb") as f:
            pdf_data = f.read()

        msg.add_attachment(
            pdf_data,
            maintype="application",
            subtype="pdf",
            filename=f"{responder["common_info"]["threat_type"]}-{state_location}.pdf",
        )

        # Attach image
        mime_type, _ = mimetypes.guess_type(img)
        if mime_type is None:
            mime_type = "application/octet-stream"

        maintype, subtype = mime_type.split("/")

        with open(img, "rb") as f:
            img_data = f.read()

        msg.add_attachment(
            img_data,
            maintype=maintype,
            subtype=subtype,
            filename=f"{responder["common_info"]["threat_type"]}-{state_location}.{subtype}",
        )

        with smtplib.SMTP(smtp_config["smtp_server"], smtp_config["smtp_port"]) as smtp:
            smtp.send_message(msg)
        print(f"Email sent to {responder["agency"]} at {contact_details[responder["agency"]]}")
        print(f"PDF stored at {pdf_report_path}")

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

def send_email(agency_res, img, location):
    for responder in agency_res:
        subject = f"Alert from ARES - {responder["common_info"]["threat_type"]} - Notifying {responder["agency"]}"
        body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height:1.4;">
                    <h2 style="color: darkred;">Alert from ARES — {responder["common_info"]["threat_type"]}</h2>
                    <p><strong>Notifying agency:</strong> {responder["agency"]}</p>
                    <p><strong>Location:</strong> {location}</p>
                    <br>
                    <h3>Details:</h3>
        """
        for key, val in responder.items():
            pretty_key = key.replace("_", " ").title()

             # 1) If it’s a list → make a sub‐bullet list
            if isinstance(val, list):
                body += f"<p><strong>{pretty_key}:</strong></p><ul>"
                for item in val:
                    body += f"<li>{item}</li>"
                body += "</ul>"

            # 2) If it’s a nested dict → drill one level deeper
            elif isinstance(val, dict):
                body += f"<p><strong>{pretty_key}:</strong></p>"
                for subkey, subval in val.items():
                    pretty_sub = subkey.replace("_", " ").title()
                    if isinstance(subval, list):
                        body += f"<p><strong>{pretty_sub}:</strong></p><ul>"
                        for item in subval:
                            body += f"<li>{item}</li>"
                        body += "</ul>"
                    else:
                        body += f"<p>{pretty_sub}: {subval}</p>"

            # 3) Otherwise it’s a primitive → just one line
            else:
                body += f"<p><strong>{pretty_key}:</strong> {val}</p>"

        body += """
                </body>
            </html>
        """

        msg = MIMEMultipart()

        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

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