import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class UserModel:
    """User data model for secure mode"""

    def __init__(self, users_file: str = 'users.json'):
        self.users_file = users_file
        self._ensure_file()

    def _ensure_file(self):
        """Ensure users file exists"""
        if not os.path.exists(self.users_file):
            default_users = {
                'admin': {
                    'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LEsBpIwEJRJTdFYXG',  # admin123
                    'is_admin': True,
                    'created_at': datetime.now().isoformat(),
                    'last_login': None,
                    'files_count': 0,
                    'total_storage': 0
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=4)

    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        users = self._load_users()
        return users.get(username)

    def create_user(self, username: str, password_hash: str, is_admin: bool = False) -> Dict:
        """Create a new user"""
        users = self._load_users()

        if username in users:
            raise ValueError("User already exists")

        user_data = {
            'password_hash': password_hash,
            'is_admin': is_admin,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'files_count': 0,
            'total_storage': 0
        }

        users[username] = user_data
        self._save_users(users)

        return user_data

    def update_user_stats(self, username: str, files_count: int, storage_used: int):
        """Update user file statistics"""
        users = self._load_users()
        if username in users:
            users[username]['files_count'] = files_count
            users[username]['total_storage'] = storage_used
            users[username]['last_login'] = datetime.now().isoformat()
            self._save_users(users)

    def list_users(self) -> List[Dict]:
        """List all users"""
        users = self._load_users()
        user_list = []
        for username, data in users.items():
            user_data = data.copy()
            user_data['username'] = username
            user_list.append(user_data)
        return user_list

    def _load_users(self) -> Dict:
        """Load users from file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_users(self, users: Dict):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)


class FileModel:
    """File metadata model for secure mode"""

    def __init__(self, metadata_file: str = 'metadata_secure.json'):
        self.metadata_file = metadata_file
        self._ensure_file()

    def _ensure_file(self):
        """Ensure metadata file exists"""
        if not os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'w') as f:
                json.dump({}, f, indent=4)

    def create_file_record(self, file_id: str, filename: str, owner: str,
                          file_size: int, encryption_key: str,
                          chunks_info: List[Dict], checksum: str) -> Dict:
        """Create a new file record"""
        metadata = self._load_metadata()

        file_record = {
            'filename': filename,
            'owner': owner,
            'file_size': file_size,
            'upload_time': datetime.now().isoformat(),
            'encryption_key': encryption_key,
            'chunks': chunks_info,
            'checksum': checksum,
            'download_count': 0,
            'last_download': None
        }

        metadata[file_id] = file_record
        self._save_metadata(metadata)

        return file_record

    def get_file_record(self, file_id: str) -> Optional[Dict]:
        """Get file record by ID"""
        metadata = self._load_metadata()
        return metadata.get(file_id)

    def get_user_files(self, username: str) -> List[Dict]:
        """Get all files owned by a user"""
        metadata = self._load_metadata()
        user_files = []

        for file_id, file_data in metadata.items():
            if file_data['owner'] == username:
                file_data_copy = file_data.copy()
                file_data_copy['file_id'] = file_id
                user_files.append(file_data_copy)

        return user_files

    def update_download_stats(self, file_id: str):
        """Update download statistics for a file"""
        metadata = self._load_metadata()
        if file_id in metadata:
            metadata[file_id]['download_count'] += 1
            metadata[file_id]['last_download'] = datetime.now().isoformat()
            self._save_metadata(metadata)

    def delete_file_record(self, file_id: str, owner: str) -> bool:
        """Delete file record if owned by user"""
        metadata = self._load_metadata()
        if file_id in metadata and metadata[file_id]['owner'] == owner:
            del metadata[file_id]
            self._save_metadata(metadata)
            return True
        return False

    def list_all_files(self) -> List[Dict]:
        """List all files (admin only)"""
        metadata = self._load_metadata()
        files_list = []

        for file_id, file_data in metadata.items():
            file_data_copy = file_data.copy()
            file_data_copy['file_id'] = file_id
            files_list.append(file_data_copy)

        return files_list

    def _load_metadata(self) -> Dict:
        """Load metadata from file"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_metadata(self, metadata: Dict):
        """Save metadata to file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4, default=str)


# Global model instances
user_model = UserModel()
file_model = FileModel()