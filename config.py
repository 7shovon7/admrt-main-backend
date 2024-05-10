import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
