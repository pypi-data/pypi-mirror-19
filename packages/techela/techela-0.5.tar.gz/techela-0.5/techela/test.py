import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()

msg['Subject'] = 'test;'
msg['From'] = 'jkitchin@andrew.cmu.edu'
msg['To'] = 'johnrkitchin@gmail.com'

body = 'got it.'

msg.attach(MIMEText(body, 'plain'))

with smtplib.SMTP_SSL('relay.andrew.cmu.edu', port=465) as s:
    s.send_message(msg)
    s.quit()
