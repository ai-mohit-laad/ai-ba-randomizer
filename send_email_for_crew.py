import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

smtp_server = 'email-smtp.ap-south-1.amazonaws.com'
smtp_port = 587
smtp_username = 'AKIA6MPHRG2WGXH7S4WD'
smtp_password = os.getenv('SES_SMTP_PASSWORD')

def send_email_to_crew(email, name):

    sender = 'ops.tech@airindia.com'
    
    name = ' '.join(word.strip().capitalize() for word in name.split())
    
    body = f"""
        <html>
        <head>
        </head>
        <body>
            <p>Dear {name},</p>

            blah blah blah
          
            <p>Thank You, and kind regards</p>

            <p>Operations Tech Team</p>

            <p>Air India D&T</p>
            
            <i>Disclaimer: Do not reply, this is an auto generated mail.</i>
        </body>
        </html>
        """

    to_emails = [email]
    # to_emails = ['testhh@airindia.com']
    test_emails = [
        'mohit.laad@airindia.com',
    ]
    cc_emails = [
    ]   
    
    message = MIMEMultipart()

    message['From'] = sender
    message['To'] = ','.join(to_emails)
    message['Cc'] = ','.join(cc_emails)
    message['Bcc'] = ','.join(test_emails)
    message['Subject'] = f'Testing of BA Randomizer'  
    message.attach(MIMEText(body, 'html'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            recipients = to_emails + cc_emails + test_emails  # Combine To and Cc recipients
            server.sendmail(sender, recipients, message.as_string())
            server.close()
            print(f"[ ]     Email sent successfully to {recipients}!")
    except Exception as ex:
        st.write(ex)
        print("exception in sending mail", ex)

