# **Kai Python Package**

## **Setup**

Run the following commands to initialise the project directory

```
python3 setup.py build
python3 setup.py install
```

## **Module Initialisation**

a. Make sure the **moduleId** and **moduleSecret** are defined correcty in your program.

```python
moduleID = "moduleName"     # Name can be anything
moduleSecret = "qwerty"     # Leave as is
```

b. Make sure the KaiSDK service is running.   
  
c. Connect to the KaiSDK Websocket.
```python
module = WebSocketModule()
success = module.connect(moduleID, moduleSecret)

if not success:
    print("Unable to authenticate with Kai SDK")
    exit(1)
```

## **Getting Data**

### **Set Capabilities**

```python
# Setting single capability
module.setCapabilities(module.DefaultKai, KaiCapabilities.AccelerometerData) 

# Setting multiple capabilities
module.setCapabilities(module.DefaultKai, KaiCapabilities.AccelerometerData | KaiCapabilities.GyroscopeData | KaiCapabilities.PYRData)
```

### **Set Listeners**

```python
def accelerometerEv(ev):
    print(ev.accelerometer.x)
    print(ev.accelerometer.y)
    print(ev.accelerometer.z_

module.DefaultKai.register_event_listener(Events.AccelerometerEvent, accelerometerEv)
```

### **Unset Capabilities**

```python
# Unsetting single capability 
module.unsetCapabilities(module.DefaultKai, KaiCapabilities.AccelerometerData)

# Unsetting multiple capabilities
module.unsetCapabilities(module.DefaultKai, KaiCapabilities.AccelerometerData | KaiCapabilities.GyroscopeData | KaiCapabilities.PYRData)
```

## **Closing the Module**

```python
module.close()
```




Run the example file using the following command
```
python3 Gesture.py
```
