"""
File upload helper for handling pet photos
"""
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

class FileUploadHelper:
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    
    @staticmethod
    def save_photo(file):
        """Save uploaded photo and return URL"""
        if not file or not file.filename:
            return None
        
        if not FileUploadHelper.allowed_file(file.filename):
            return None
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        return f'/uploads/{filename}'
    
    @staticmethod
    def delete_photo(photo_url):
        """Delete photo file"""
        if not photo_url:
            return
        
        photo_path = os.path.join(current_app.root_path, photo_url.lstrip('/'))
        if os.path.exists(photo_path):
            os.remove(photo_path)
