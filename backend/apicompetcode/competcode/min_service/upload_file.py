from competcode import UPLOAD_FOLDER
from werkzeug.utils import secure_filename
import os
def upload(file):
    filename = None

    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        
        file.save(path)
    return filename    