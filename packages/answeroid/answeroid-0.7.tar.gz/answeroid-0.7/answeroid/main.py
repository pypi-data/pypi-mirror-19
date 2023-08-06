import threading
from answeroid.droid import Answeroid
from helpers.gcal import Gcal
from helpers.wolf import Wolf
# from helpers.bing import Bing
from sites.pa import PA


class BotThread(threading.Thread):
    def __init__(self, site, helper):
        threading.Thread.__init__(self)
        self.droid = Answeroid(site, helper)
        self.run = self.droid.watch


with PA() as ste:
    gcal = BotThread(ste, Gcal())
    wolf = BotThread(ste, Wolf())
    gcal.start()
    wolf.start()
    gcal.join()
    wolf.join()
