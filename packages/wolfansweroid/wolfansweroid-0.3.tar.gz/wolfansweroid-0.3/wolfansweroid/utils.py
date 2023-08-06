import os


def get_wolf_app_id():
    return os.environ.get('WOLF_APP_ID', 'YOUR_WOLF_API_KEY_HERE')
