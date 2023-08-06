import wolframalpha
from helpers import utils


class Wolf:
    def __init__(self):
        self.wa = wolframalpha.Client(utils.get_wolf_app_id())

    def create_reply(self, content):
        _, *wolf_query = content.split('WOLF:')
        wolf_query = wolf_query[0].split('\n')[0]  # A new line denotes end of query
        wolf_results = self.wa.query(wolf_query)
        try:
            results = [(sub['plaintext'], sub['img']['@src']) for pod in wolf_results.pods for sub in pod.subpods]
        except AttributeError:
            results = []
        return utils.SUCCESS_TEMPLATE % ('\n'.join(['{}\n[img]{}[/img]'.format(str(text), str(img)) for (text, img) in results])) if results else utils.FAILURE_TEMPLATE % wolf_query
