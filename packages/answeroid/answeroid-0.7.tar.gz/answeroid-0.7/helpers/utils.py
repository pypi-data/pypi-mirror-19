import os


def get_wolf_app_id():
    return os.environ.get('WOLF_APP_ID', 'YOUR_WOLF_API_KEY_HERE')

TEMPLATES = {
    'WOLF': {
        'SUCCESS': '\[\color{blue}{\\textbf{Expression:}}\]%s' \
                   '\[\color{green}{\\textbf{Computed:}}\]%s' \
                   '\[\\textbf{Plaintext:}\]%s',
        'FAILURE': '\[\color{red}{\\textbf{Unable to compute:}}\]%s'
    },
    'GCAL': {
        'SUCCESS': '\[\color{blue}{\\textbf{Expression:}}\]%s' \
                   '\[\color{green}{\\textbf{Computed:}}\]%s' \
                   '\[\\textbf{Plaintext:}\]%s',
        'FAILURE': '\[\color{red}{\\textbf{Unable to compute:}}\]%s'
    }
}
