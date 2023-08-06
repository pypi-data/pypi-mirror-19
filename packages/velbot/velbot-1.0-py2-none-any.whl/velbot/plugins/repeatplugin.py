from rtmbot.core import Plugin
from rtmbot.core import Job

class RepeatJob(Job):

    def __init__(self,interval,debug):
        Job.__init__(self,interval )
        if debug:
            self.debug = True
        self.output = []

    def run(self, slack_client):
        self.output = []
        self._dbg("{}:Job Running...".format(self.__class__.__name__)) 
        self.output.append(["#announcements", "Repeating..."])
        return self.output

class RepeatPlugin(Plugin):

    def register_jobs(self):
        job = RepeatJob(10, debug=True)
        self.jobs.append(job)
