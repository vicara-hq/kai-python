from websocket import create_connection
import websocket
import json

subscribed_capabilities = {
    "type": "setCapabilities"
}

global ws

def connect_sdk():
    websocket.enableTrace(True)
    try:
        ws = create_connection('ws://localhost:2203')
        # return(ws)
    except Exception as error:
        print('Caught this error: ' + repr(error))
        return(None)

def subscribe_capabilities( capabilities ):

    # ws = connect_sdk()

    if( type(capabilities) is list ):
        for i in capabilities:
            subscribed_capabilities[str(i)] = True

        try:
            ws.send(json.dumps(subscribed_capabilities))
        except Exception as error:
            print('Caught this error: ' + repr(error))

    else:
        return("Wrong format, must be a list")

def unsubscribe_capabilities( capabilities ):

    # ws = connect_sdk()

    if( type(capabilities) is list ):
        for i in capabilities:
            subscribed_capabilities[str(i)] = False
        ws.send(json.dumps(subscribed_capabilities))

