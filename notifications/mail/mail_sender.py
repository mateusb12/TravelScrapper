# Create a function that sends email to a user
import smtplib


def send_email(email: str, message: str):
    # Create a SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # Start TLS for security
    s.starttls()
    # Authentication
    s.login("email", "password")
    # Message to be sent
    message = "Subject: {}\n\n{}".format(subject, message)
    # Sending the mail
    s.sendmail("email", email, message)
    # Terminating the SMTP session
    s.quit()
    print(colored("Email sent!", "green"))
    return True