import requests


class Site:
    def __init__(self, username, password, urls=None):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.get = self.session.get
        self.post = self.session.post
        self.urls = urls  # Optional handy constant for various urls

    # Needed to be able to use with User() as u:
    def __enter__(self):
        self.login()
        return self

    # Needed to be able to use with User() as u:
    def __exit__(self, typ, value, traceback):
        resp = self.logout()
        self.session.close()
        return resp

    def login(self):
        raise NotImplementedError('Various sites have different login mechanisms')

    def logout(self):
        raise NotImplementedError('Various sites have different logout mechanisms')

    def get_viewing_question(self):
        raise NotImplementedError('Implement this in the subclass - return the question id being viewed')

    def get_replies(self, question_id):
        raise NotImplementedError(
            'Implement this in the subclass - return a dictionary of answer ids mapped to answer contents'
        )

    def edit_reply(self, reply_id, reply_content, question_id):
        raise NotImplementedError(
            'Which answers should we edit and what should the new contents be?'
        )