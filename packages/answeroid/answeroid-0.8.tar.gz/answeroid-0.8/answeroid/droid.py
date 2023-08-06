import logging
import random
import time

logger = logging.getLogger('Bot Log')


# FIXME: Add proper docstrings
class Answeroid:
    def __init__(self, site, helper):
        # A site where you're answering (maybe hook in facebook messenger??)
        self.site = site
        # A helper bot that can retrieve answers (say from google, bing, wolfram, etc)
        self.helper = helper

    @staticmethod
    def wait(duration=None):
        wait = duration if duration is not None else random.randint(5, 10)
        logger.info('Waiting for %d seconds' % wait)
        time.sleep(wait)

    def watch(self):
        # FIXME: A better way of doing this? Subscribe?
        while True:
            # FIXME: Extract question id retrieval to site logic, retrieve question_id only, not half broken links
            question = self.site.get_viewing_question()
            if question:
                my_replies = self.site.get_replies(question)
                self._edit_replies(my_replies, question.split('/')[-1])  # Also pass the question id
            self.wait()

    def _edit_replies(self, replies, question_id):
        # replies is a dictionary of reply_id: reply_content
        # question_id is just a string with the question_id
        relevant = {_id: content for (_id, content) in replies.items()
                    if self.helper.__class__.__name__.upper()+':' in content}
        replies = {_id: self.helper.create_reply(content) for (_id, content) in relevant.items()}
        for _id, content in replies.items():
            self.site.edit_reply(_id, content, question_id)