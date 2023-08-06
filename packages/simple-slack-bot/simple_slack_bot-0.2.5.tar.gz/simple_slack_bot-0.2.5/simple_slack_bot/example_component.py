from simple_slack_bot import SimpleSlackBot

class ExampleComponent():
    def hello(self, dictionary):
        return "Hello"


    def public_channels_messages(self, dictionary):
        return "Public Channel Message"


    def private_channels_messages(self, dictionary):
        return "Private Channel Message"


    def mentions(self, dictionary):
        return "Mention"


    def direct_messages(self, dictionary):
        return "Direct Message"
