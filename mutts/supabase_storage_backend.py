import os
import mimetypes
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client
import logging

logger = logging.getLogger(__name__)

class SupabaseStorage(Storage):

    def _save(self, name, content):
        path = self._get_path(name)
        content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
        
        # Make sure content is at the start
        content.open()
        
        self.client.storage.from_(self.supabase_bucket).upload(
            path,
            content.file,  # Use the raw in-memory file
            {
                "content-type": content_type,
                "x-upsert": "true"
            }
        )
        return name

    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase_bucket = os.getenv("SUPABASE_BUCKET", "product-images")
        self.path_prefix = os.getenv("SUPABASE_PATH_PREFIX", "products/")
        self.client = create_client(self.supabase_url, self.supabase_key)

    def _get_path(self, name):
        if name.startswith(self.path_prefix):
            return name
        return f"{self.path_prefix}{name}"


    def _open(self, name, mode='rb'):
        response = self.client.storage.from_(self.supabase_bucket).download(self._get_path(name))
        return ContentFile(response)

 








    def exists(self, name):
        try:
            self.client.storage.from_(self.supabase_bucket).get_public_url(self._get_path(name))
            return True
        except Exception:
            return False

    def url(self, name):
        return f"{self.supabase_url}/storage/v1/object/public/{self.supabase_bucket}/{self._get_path(name)}"
