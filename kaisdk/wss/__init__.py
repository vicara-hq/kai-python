from websocket import create_connection
import websocket
import json

host = "localhost"
port = 2203
buf = 1024
addr = (host,port)

websocket.enableTrace(True)
ws = create_connection('ws://localhost:2203')

print "Websocket active."
print "address:\t"+host+":"+str(port)

global_capabilities = [
    "gestureData",
    "fingerShortcutData",
    "quaternionData",
    "pyrData"
]

subscribed_capabilities = {
    "type": "setCapabilities",
    "gestureData": False,
    "fingerShortcutData": False,
    "quaternionData": False,
    "pyrData": False
}

def set_capabilities( capabilities ):

    if( type(capabilities) is list ):
        for i in capabilities:
            try:
                subscribed_capabilities[str(i)] = True
            except ValueError:
                return("Wrong Format")

            ws.send(json.dumps(subscribed_capabilities))

    else:
        return("Wrong format, must be a list")

def receive_data():
    result = ws.recv()
    return('Result: {}'.format(result))
