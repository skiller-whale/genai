import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    JSON_DATA_FILE = os.path.join(os.path.dirname(__file__), 'src', 'data', 'posts.json')