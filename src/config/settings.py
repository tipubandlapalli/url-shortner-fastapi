import os
import json
import boto3

from dotenv import load_dotenv

if os.getenv("APP_ENV", "DEV") == "DEV":
    load_dotenv()
else:
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(
        SecretId=os.environ["SECRET_NAME"]
    )
    secret = json.loads(response["SecretString"])
    os.environ.update({k:str(v) for k, v in secret.items()})


class Settings:
    EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "console") 
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = os.getenv("SMTP_PORT","587")
    EMAIL_FROM = os.getenv("EMAIL_FROM")
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local") # or s3
    LOCAL_STORAGE_UPLOAD_DIR = os.getenv("LOCAL_STORAGE_UPLOAD_DIR", "uploads")
    S3_BUCKET = os.getenv("S3_BUCKET")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "286dd1caf934fdfb1f49da08c7e7b32f46caafc9a72bda94cee8010d1cb12a1f") # use safe
    JWT_ALGO = os.getenv("JWT_ALGO", "HS256")

    DB_URL = os.getenv("DB_URL", "sqlite:///todos.db")
    
settings = Settings()