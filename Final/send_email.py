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

    # Add title
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

def send_email(payload, img, agencies, location):

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