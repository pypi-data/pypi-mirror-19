from rtmbot.core import Plugin

class VelbotCorePlugin(Plugin):

    def catch_all(self, data):
        pass

    def process_text(self, data):
        self._dbg("{}:Received - {}".format(self.__class__.__name__,data)) 
        self.outputs.append([data.getlist('channel_name')[0], "Welcome to Velocity Chatbot..."]) 
        self.outputs.append([data.getlist('channel_name')[0], "You can use\"velbot help\" to get a list of commands to execute"]) 
