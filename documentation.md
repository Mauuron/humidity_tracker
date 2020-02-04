# Documentation

### Table of contents:
1. Set up the Raspberry Pi and the DHT22 sensor
2. Create ThingSpeak-channel
3. Python script
3. Run script when booting Raspberry Pi
4. Create IFTTT-applet
6. Create Thingspeak React and ThingHTTP



### 1. Set up the Raspberry Pi and the DHT22 sensor


### 2. Create Thingspeak-channel


### 3. Python script

First of all, you have to install some packages. Run following commands on your Raspberry Pi:

```
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl git

git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python setup.py install

sudo pip install thingspeak
```

If you´re working with the shell, you can create a new python-file with the following command:

```
cd Documents
sudo nano humidity_tracker.py
```

Add the following code to the file. Save with CTRL-O and close with CTRL-X.

```python
import thingspeak
import time
import Adafruit_DHT
 
channel_id = #Enter your CHANNEL_ID
write_key  = 'WRITE_API' #Enter your write api
read_key   = 'READ_API' #Enter your read api
pin = RASPBERRY_PI_PIN #Enter the number of the pin you´re using
sensor = Adafruit_DHT.DHT22 #If you´re using the DHT22
 
def measure(channel):
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        
        # write
        response = channel.update({'field1': temperature, 'field2': humidity}) #adjust according to your channel
        
        # read
        read = channel.get({})
        print("written")
        
    except:
        print("connection failed")
 
 
if __name__ == "__main__":
    channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
    while True:
        measure(channel)
        time.sleep(60) #time in seconds between reading, minimum 15 
```

### 4. Run script when booting Raspberry Pi

To automatically run your script when you´re booting your Raspberry Pi, run the following command:

```
sudo nano /etc/profile
```

Now, scroll to the bottom and add the following line, depending on the path of your file:

```
sudo python /home/pi/Documents/humidity_tracker.py
```


### 5. Create IFTTT-applet


### 6. Create Thingspeak React and ThingHTTP
