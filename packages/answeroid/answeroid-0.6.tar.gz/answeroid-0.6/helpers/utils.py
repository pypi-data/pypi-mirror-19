import os


def get_wolf_app_id():
    return os.environ.get('WOLF_APP_ID', 'YOUR_WOLF_API_KEY_HERE')

SUCCESS_TEMPLATE = 'Computed results %s'
FAILURE_TEMPLATE = 'Unable to compute {%s}'
