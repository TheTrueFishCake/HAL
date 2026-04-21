import os, zipfile
from datetime import datetime

ENV_DIR = "/path/to/env"
ARCHIVE_DIR = "/home/youruser/web/thebearminimum.net/public_html/archives"

os.makedirs(ARCHIVE_DIR, exist_ok=True)

name = datetime.now().strftime("%Y-%m-%d") + ".zip"
zip_path = os.path.join(ARCHIVE_DIR, name)

if os.path.exists(zip_path):
    exit()

with zipfile.ZipFile(zip_path, 'w') as z:
    for root, dirs, files in os.walk(ENV_DIR):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ENV_DIR)
            z.write(full, rel)
