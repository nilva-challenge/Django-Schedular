from django.core.mail import EmailMessage
from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    def send_email(self, subject, message, from_email, recipient_list):
        pass


class RealEmailService(EmailService):
    def send_email(self, subject, message, from_email, recipient_list):
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()


class MockEmailService(EmailService):
    def send_email(self, subject, message, from_email, receiver):
        print(f"Mock email sent: Subject - {subject}, Recipients - {receiver}")
