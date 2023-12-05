# Holds functions for sending mail

# app.py
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

# Configure Flask app to use Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

class EmailSender:
    @staticmethod
    def send_email(to, subject, body, sendAsHTML):
        try:
            if (sendAsHTML):
                msg = Message(
                    subject=subject,
                    recipients=[to],
                    body=body
                )
            else:
                msg = Message(
                    subject=subject,
                    recipients=[to],
                    body=body
                )
                
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

if __name__ == '__main__':
    app.run(debug=True)
