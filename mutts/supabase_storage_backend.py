import os
import mimetypes
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client
import logging

logger = logging.getLogger(__name__)

class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase_bucket = os.getenv("SUPABASE_BUCKET", "product-images")
        self.path_prefix = os.getenv("SUPABASE_PATH_PREFIX", "products/")
        self.client = create_client(self.supabase_url, self.supabase_key)

    def _get_path(self, name):
        return f"{self.path_prefix}{name}"

    def _open(self, name, mode='rb'):
        response = self.client.storage.from_(self.supabase_bucket).download(self._get_path(name))
        return ContentFile(response)

    def _save(self, name, content):
        path = self._get_path(name)
        content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
        
        # Read the content into memory as bytes
        content.open()
        file_data = content.read()

        # Upload to Supabase
        logger.info(f"Uploading {path} to bucket {self.supabase_bucket}")
        res = self.client.storage.from_(self.supabase_bucket).upload(
            path,
            file_data,
            {"content-type": content_type, "upsert": True}
        )

        logger.info(f"Upload result: {res}")
        return name

    def exists(self, name):
        try:
            self.client.storage.from_(self.supabase_bucket).get_public_url(self._get_path(name))
            return True
        except:
            return False

    def url(self, name):
        return f"{self.supabase_url}/storage/v1/object/public/{self.supabase_bucket}/{self._get_path(name)}"
