from bs4 import BeautifulSoup
import json
import os
from sites.common import Site


class PA(Site):
    def __init__(self, username=None, password=None, urls=None):
        username = username or os.environ.get('PA_USER', '')
        password = password or os.environ.get('PA_PASS', '')
        urls = urls or URLS()
        Site.__init__(self, username, password, urls)

    def login(self):
        data = {'username': self.username,
                'password': self.password,
                'keep': 'on'}
        return self.session.post(self.urls.login, data=data, allow_redirects=True)

    def logout(self):
        return self.session.get(self.urls.logout)

    def get_viewing_question(self):
        user_url = self.urls.get_user_url(self.username)
        response = self.get(user_url)
        response_json = json.loads(response.content.decode())
        question = response_json.get('isDoing', {}).get('link')
        return question if question and question.startswith('/question/') else None

    def get_replies(self, question):
        question_page = self.get(self.urls.get_question_url(question))
        soup = BeautifulSoup(question_page.content, 'html.parser')
        answers = soup.find_all('div', {'class': 'MyAnswerDisplay PostContainer boxShadow_light '}) # space
        return {a.attrs['data-id']: a.find('div', {'class': 'MyAnswerContent'}).attrs['data-content'] for a in answers}

    def edit_reply(self, reply_id, reply, question_id):
        self.post(self.urls.edit_answer, data={'answer_id': reply_id, 'content': reply, 'question_id': question_id})


class URLS:
    def __init__(self):
        self.url = 'https://www.peeranswer.com/'
        self.login = self.url + 'login'
        self.logout = self.url + 'logout'
        self.edit_answer = self.url + 'answer/edit'

    def get_user_url(self, username):
        return self.url + 'user/%s?_=0' % username

    def get_question_url(self, question):
        return self.url + question[1:]