import smtplib
from email.mime.text import MIMEText


def send_mail(movie_name, email, message):
    port = 465
    smtp_server = 'smtp.mailtrap.io'
    login = 'a72c76b228385b'
    password = '4fbf409d3afbd4'
    message = f"<h3>New Contact-info Submission</h3><ul><li>Movie Name: {movie_name}</li><li>Email: {email}</li><li>Message: {message}</li></ul>"

    sender_email = 'hritikadhikari05@gmail.com'
    receiver_email = 'hritikadhikari05@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = f'New Message from  {email}'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())