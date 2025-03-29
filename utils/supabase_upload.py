import os
import mimetypes
from supabase import create_client
from django.utils.text import slugify  # this safely removes/normalizes characters

def upload_to_supabase(file):
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "product-images")
    SUPABASE_PATH_PREFIX = os.getenv("SUPABASE_PATH_PREFIX", "products/")
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    file.seek(0)  # Ensure it's at the beginning
    original_name = file.name
    base_name, ext = os.path.splitext(original_name)
    safe_filename = slugify(base_name) + ext.lower()  # e.g., 'augmented-reality.jpg'
    
    full_path = f"{SUPABASE_PATH_PREFIX}{safe_filename}"
    content_type = mimetypes.guess_type(safe_filename)[0] or "application/octet-stream"
    file_data = file.read()
    print(f"[UPLOADING] {safe_filename} to {full_path}")
    print("ORIGINAL NAME CONTENT TYPE FILE DATA", original_name, content_type, file_data)
    # Upload to Supabase
    client.storage.from_(SUPABASE_BUCKET).upload(
        path=full_path,
        file=file_data,
        file_options={
            "content-type": content_type,
            "x-upsert": "true"
        }
    )
    
    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{full_path}"
    print(f"[URL] {public_url}")
    return public_url

