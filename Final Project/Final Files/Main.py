# -----------------------imports-----------------

import streaming
import pyttsx

# -----------------------------------------------

# ------------------------variables--------------
name = "Amy"

# -----------------------------------------------


# ------------------------commands---------------
class command_class(object):
    def __init__(self, command):
        self.engine=pyttsx.init()
        self.command = command
        self.command_analyzer()

    def command_analyzer(self):
        if name + " say hello world" in self.command:
            self.hello_world()

    ###TODO create function to analyze the command and send it on its way example: internal something that doesnt use internet
    def hello_world(self):
        self.engine.say("Hey There")
        self.engine.runAndWait()
#--------------------------------------------------

def main():
    while True:
        command = streaming.main()
        if name in command:
            x = command_class(command)


if __name__ == '__main__':
    main()
