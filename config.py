import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
