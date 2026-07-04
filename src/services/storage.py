import os, shutil
from pathlib import Path

from fastapi import UploadFile, HTTPException, status
from typing import Protocol
from uuid import uuid4

from src.config.settings import settings

import boto3

class StorageService(Protocol):
    
    def upload(self, file:UploadFile, user_id: str) -> str:
        ... 

class LocalStorageService(StorageService):
    def __init__(self, upload_dir):
        self.upload_dir = upload_dir
    
    def upload(self, file:UploadFile, user_id: str) -> str:
        suffix = Path(file.filename or "").suffix
        if not suffix:
            raise HTTPException(detail="invalid file type", status_code=status.HTTP_400_BAD_REQUEST)
        destination = Path(
            self.upload_dir /
            "profile-pics" /
            user_id / 
            f"user-{uuid4().hex}{suffix}"
        )
        destination.parent.mkdir(exist_ok=True, parents=True)

        file.file.seek(0)

        with open(destination, "wb") as target:
            shutil.copyfileobj(file.file, target)
        
        return str(destination)
    
class S3StorageService(StorageService):
    def __init__(self, bucket, region):
        self.bucket = bucket
        self.region = region

    def upload(self, file:UploadFile, user_id: str) -> str:
        kwargs = {
            "region_name":self.region
        }

        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
            kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY

        client = boto3.client("s3",**kwargs)
        
        file.file.seek(0)
        suffix = Path(file.filename or "").suffix
        if not suffix:
            raise HTTPException(detail="invalid file type", status_code=status.HTTP_400_BAD_REQUEST)

        key = f"uploads/profile-pics/{user_id}/user-{uuid4().hex}{suffix}"

        client.upload_fileobj(
            file.file, 
            self.bucket, 
            key,
            ExtraArgs={
                "ContentType":file.content_type or "application/octet-stream"
            }
        )

        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
def get_storage_service() -> StorageService:
    if settings.STORAGE_BACKEND == "local":
        if settings.LOCAL_STORAGE_UPLOAD_DIR is None:
            raise RuntimeError("LOCAL_STORAGE_UPLOAD_DIR is required for local storage")
        return LocalStorageService(settings.LOCAL_STORAGE_UPLOAD_DIR)
    elif settings.STORAGE_BACKEND == "s3":
        if settings.S3_BUCKET and settings.AWS_REGION:
            return S3StorageService(settings.S3_BUCKET, settings.AWS_REGION)
        else:
            raise RuntimeError("S3_BUCKET, AWS_REGION  is required for s3 storage")
    raise ValueError(
        f"Unknown STORAGE_BACKEND: {settings.STORAGE_BACKEND}"
    )