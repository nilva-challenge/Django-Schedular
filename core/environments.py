from os import environ
from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(int(environ.get('DEBUG', 0)))
SECRET_KEY = environ.get('SECRET_KEY')
ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', ' ').split()

EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = environ.get('DEFAULT_FROM_EMAIL')

