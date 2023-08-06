class HelloWorldComponent():
    def hello(self, dictionary):
        print("HelloWorldComponent received hello event")


    def mentions(self, dicitonary):
        return "mention"


    def public_channels(self, dictionary):
        return "public channel"


    def direct_messages(self, dictionary):
        return "direct message"
