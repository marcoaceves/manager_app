
import smtplib

from email.message import EmailMessage





def send_email(receiver):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Make sure to give app access in your Google account
    server.login('ahf.task.manager@gmail.com', '')
    email = EmailMessage()
    email['From'] = 'ahf.task.manager@gmail.com'
    email['To'] = receiver
    email['Subject'] = 'AHF TAKS MANAGER'
    email.set_content("hello world")
    server.send_message(email)

send_email('')




