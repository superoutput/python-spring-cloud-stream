import json, os
from enum import Enum
from spring.message import Message
from aenum import extend_enum
import hmsutils._global_var as _global_var

class MessageFactory(object):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Initialise Message Dict
    with open(base+'/hmsutils/stdmessagesettings.json') as json_data:
        json_string = json.load(json_data)

    def console(self, txt):
        print(txt)

    def __init__(self):
        ms = _global_var._global_ctx['Microservice_Name']
        self.ms = ms
        self.settings = self.json_string[ms]
        self.message = Enum('Message', ' '.join(self.json_string[ms]))

        for i, key in enumerate(self.json_string[ms].keys()):
            extend_enum(Message, key, self.json_string[ms][key])

    def get_messages(self):
        return self.message

    def get(self, message):
        return self.settings[message.name]

    def show_all(self):
        for message in self.message:
            print('{:15} = {}'.format(message.name, message.value))

