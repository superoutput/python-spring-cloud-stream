from spring.streamsubscriber import StreamSubscriber

class Client(StreamSubscriber):

    def postConstruct( self ):
        # TODO Connection is connected. You can override function postConstruct()."
        pass

    def onMessage( self, message ):
        print('New Message :', message)

if __name__ == "__main__":
    try:
        client = Client()
    except (SyntaxError, NameError) as e:
        print(e)