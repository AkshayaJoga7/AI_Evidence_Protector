import os
import uuid
from werkzeug.utils import secure_filename
from config import Config
from utils.security import generate_file_sha256

class StorageService:
    @staticmethod
    def save_upload(file_obj, file_type: str) -> dict:
        """
        Save uploaded file securely to designated upload folder.
        Returns dictionary with file metadata and digital hash.
        """
        if file_type == 'image':
            target_dir = Config.IMAGE_UPLOADS
        elif file_type == 'audio':
            target_dir = Config.AUDIO_UPLOADS
        else:
            target_dir = Config.UPLOAD_FOLDER

        os.makedirs(target_dir, exist_ok=True)
        
        original_name = secure_filename(file_obj.filename)
        ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else ''
        unique_filename = f"{uuid.uuid4().hex}_{original_name}"
        full_path = os.path.join(target_dir, unique_filename)

        file_obj.save(full_path)

        # Generate cryptographic integrity hash
        file_hash = generate_file_sha256(full_path)

        return {
            "original_filename": original_name,
            "filename": unique_filename,
            "file_path": full_path,
            "file_hash": file_hash,
            "file_type": file_type
        }
