# Python code to illustrate Sending mail from
# your Gmail account
import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login("karishmachanglani@gmail.com", "Kc1212kmc")

# message to be sent
message = "Message_you_need_to_send"

# sending the mail
to = {"karishmachanglani@gmail.com", "karishmachanglani@boomi.com"}
s.sendmail("sender_email_id", to, message)

# terminating the session
s.quit()

