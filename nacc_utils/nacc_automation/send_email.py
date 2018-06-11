import smtplib
import errno
import sys
import ConfigParser

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CONFIG_PATH = "./smtp_config_example.ini"


def read_config(config_path):
    config = ConfigParser.ConfigParser()
    try:
        config.readfp(open(config_path, "r"))
    except IOError as ioerror:
        if ioerror.errno == errno.ENOENT:
            print >> sys.stderr, "The file could not be found."
            print >> sys.stderr, "Please check that %s exists" % config_path
        raise ioerror
    except Exception as ex:
        print >> sys.stderr, "An error occurred #vague"
        print >> sys.stderr, ex
        raise ex
    return config


def send_email(subject, message):
    """
    This functions generates an email with a given subject and
    html formatted message.
    Arguments:
    subject: string representing the email subject
    message: an HTML string used as the content of the email
    """

    config = read_config(CONFIG_PATH)
    my_address = config.get('credentials', 'my_address')
    recipient = config.get('recipient_list', 'recipients')
    recipient = recipient.split(",")
    mime_message = MIMEText(message.encode('utf-8'), 'html', 'utf-8')
    print("Sending email to: ")
    print(recipient)

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.ufl.edu')

    # If an authenticated account is needed
    # password = config.get('credentials', 'password')
    # s.starttls()
    # s.login(my_address, password)

    # For each contact, send the email:
    for email in recipient:
        msg = MIMEMultipart()       # create a message

        # setup the parameters of the message
        msg['From'] = my_address
        msg['To'] = email
        msg['Subject'] = subject

        # add in the message body
        msg.attach(mime_message)

        # send the message via the server set up earlier.
        s.sendmail(my_address, email, msg.as_string())
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()
