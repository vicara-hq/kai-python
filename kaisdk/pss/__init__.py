import websocket
import json

subscribed_capabilities = {
    "type": "setCapabilities"
}

try:
    #TODO: Check for Process Server
except:
    print('Sdk seems to be disabled, Consider Restarting.')

def send_data(data):
    # Send data for process server

def subscribe_capabilities( capabilities ):

    # ws = connect_sdk()

    if( type(capabilities) is list ):
        for i in capabilities:
            subscribed_capabilities[str(i)] = True
        try:
            send_data( json.dumps(subscribed_capabilities) )
        except Exception as error:
            print('Caught this error: ' + repr(error))

    else:
        return("Wrong format, must be a list")

def unsubscribe_capabilities( capabilities ):

    if( type(capabilities) is list ):
        for i in capabilities:
            subscribed_capabilities[str(i)] = False
        send_data( json.dumps(subscribed_capabilities) )

def get_data():
    # Receive data from process server
    # return(ws.recv())
