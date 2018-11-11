import json

subscribed_capabilities = {
    "type": "setCapabilities"
}

# try:
#     websocket = websockets.connect('ws://localhost:2203') 
#     # print("Done")
# except:
#     print('Sdk seems to be disabled, Consider Restarting.')

# async def send_data(data):
#     await websocket.send(data)
#     return("Data Sent")

# async def get_data():
#     recv_data = await websocket.recv()
#     return(recv_data)

async def subscribe_capabilities( capabilities ):

    if( type(capabilities) is list ):
        for i in capabilities:
            subscribed_capabilities[str(i)] = True
        
        return( json.dumps(subscribed_capabilities) )    
        # except Exception as error:
        #     print('Caught this error: ' + repr(error))
    else:
        return("Wrong format, must be a list")

def unsubscribe_capabilities( capabilities ):

    if( type(capabilities) is list ):
        for i in capabilities:
            subscribed_capabilities[str(i)] = False
        send_data( json.dumps(subscribed_capabilities) )
