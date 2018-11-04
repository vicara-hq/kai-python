def is_authourized():
    return(False)

if(is_authourized):
    from . import pss
    from . import wss

else:
    print("No auth")