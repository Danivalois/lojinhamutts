import os
import mimetypes
import requests
from django.core.files.storage import Storage
from django.conf import settings

class SupabaseStorage(Storage):
    def __init__(self):
        self.bucket = os.getenv("SUPABASE_BUCKET", "product-images")
        self.project_url = os.getenv("SUPABASE_URL")
        self.api_key = os.getenv("SUPABASE_SERVICE_KEY")
        self.headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}"
        }

    def _get_upload_url(self, name):
        return f"{self.project_url}/storage/v1/object/{self.bucket}/{name}"

    def _open(self, name, mode='rb'):
        response = requests.get(self._get_upload_url(name), headers=self.headers)
        if response.status_code == 200:
            return response.content
        raise FileNotFoundError(f"File not found on Supabase: {name}")

    def _save(self, name, content):
        upload_url = f"{self.project_url}/storage/v1/object/{self.bucket}/{name}"
        mime_type, _ = mimetypes.guess_type(name)
        files = {
            'file': (name, content.read(), mime_type or 'application/octet-stream')
        }
        response = requests.post(
            f"{self.project_url}/storage/v1/upload",
            headers=self.headers,
            params={"bucket": self.bucket, "path": name, "upsert": "true"},
            files=files
        )
        if response.status_code not in [200, 201]:
            raise Exception(f"Supabase upload failed: {response.text}")
        return name

    def exists(self, name):
        response = requests.head(self._get_upload_url(name), headers=self.headers)
        return response.status_code == 200

    def url(self, name):
        return f"{self.project_url}/storage/v1/object/public/{self.bucket}/{name}"
