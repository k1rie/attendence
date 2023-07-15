import uuid

import cloudinary
from cloudinary.uploader import upload

from src.config import settings


class CloudinaryUploader:
    @staticmethod
    def upload_file(filename, folder="/attendance-reports"):
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_secret_key
        )
        report_id = str(uuid.uuid4())

        upload_result = upload(filename, folder=folder, filename_override=f"$report-{report_id}.xlsx",
                               resource_type="raw")

        return upload_result["url"]
