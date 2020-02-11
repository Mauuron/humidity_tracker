# Documentation

### Table of contents:
1. Setup the Raspberry Pi and the DHT22 sensor
2. Create ThingSpeak-channel
3. Python script
3. Run script when booting Raspberry Pi
4. Create IFTTT-applet
6. Create Thingspeak React and ThingHTTP
7. **Addition**: Two sensors and check for invalid values



### 1. Setup the Raspberry Pi and the DHT22 sensor

With the sensor, there comes a quite good documentation what the different pins are. I would suggest you to buy the the sensor already soldered with the resistor, so you have only three pins.

I glued a small breadboard on top of my Raspberry Pi case and simply plugged the sensor in. 
From left to right, the pins of the sensor mean the following:

| number | meaning |
|:------:|---------|
| 1      | VCC     |
| 2      | DATA    |
| 3      | GROUND  |

Connect pin 1 with a *3V3 power* pin of your Raspberry Pi, pin 2 with the *GPIO pin* you want to use and pin 3 obviously with a *Ground* pin of your Raspberry Pi.

And thats basically the whole setup. Admittedly, that does not look very nice, but it does what it´s supposed to do.

### 2. Create Thingspeak-channel

Navigate to Channels > My Channels and press "New Channel". Enter your prefered name and a description if you like. Tick the number of fields you want to use. In this example, tick two and name them something like "humidity" and "temperature". Leave the remaining fields empty and press "Save Channel".

Now, open your new channel and navigate to "API Keys". Write down both the Write API Key and the Rad API Key. On the top of the site you also find your Channel ID. Write that down as well.

If you like, you can make lots of adjustments to your charts by clicking on the pen next to the X in the chart. For example since I measure every 60 seconds, I plot 2880 results in total to always see the course of the last two days. Additionally, I set "Average" to 15, which means ThingSpeak takes data from 15 minutes and then plots the average. I have done this because the graph looks a lot nicer like that. Further I have set "Rounding" to 3 because the sensor is not that precise anyway. 

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
You also find the code as a python file in the repository.

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

I suggest you to not measure more than once every minute, because otherwise you´re creating lots of data and the temperature and humidity wont change that much in one minute that you are losing important data.

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

If your script is running, you should already see your data being plotted in the ThingSpeak channel. Now, we want to create a IFTTT-applet to get smartphone notifications when for example the humidity exceeds a certain value.

Go to ifttt.com, sign in and navigate to "Create". Press on "this", search for the service "Webhooks" and select "Receive a web request" as the trigger. Enter an event name and write that one down, we will need that in step 6 again (for example humidity_alert)

Now press on "that", search for the service "Notification" and select "Send a **rich** notification from the IFTTT app" as the action. Enter a title of the notification and write your preferred message. Additionally to just the alert that the humidity is too high, I wanted IFTTT to tell me the exact values of the curret humidity and temperature, so my message is:

**"The event {{EventName}} occurred! Humidity: {{Value1}}%, temperature: {{Value2}}°C. Better open a window!"**

The values are not rounded in the notification (!) but I don´t know how to set that up. Let me know if anyone figured that out.

After your applet has been saved, navigate to Explore and search for Webhooks. Click on "services" and then on "Webhooks". Now navigate to "Documentation" (top right corner). You should now see a page with the title "To trigger an Event". Copy and save the url to make a POST or GET web request. It should look like that: "https://maker.ifttt.com/trigger/{event}/with/key/YOUR_KEY". Now we can set up the web request via ThingSpeak.

### 6. Create ThingSpeak React and ThingHTTP

Go back to thingspeak.com and navigate to Apps > ThingHTTP and press "New ThingHTTP". Enter a prefered name and the url you have just saved in the field "URL:". Make sure the url ends with your key and replace the {event} with your event name, in my example **humidity_alert**. Set the method to **POST** and the content type to **Application/json**. Set the body to **{ "value1" : "%%channel_CHANNELID_field_2%%", "value2": "%%channel_CHANNELID_field_1%%"}** and replace **CHANNELID** with your ID. Adjust the field numbers so that value1 is the humidity and value2 the temperature. Now you can save the ThingHTTP.

Last but not least, we need to create a trigger. Navigate to Apps > React and press "New React". Again enter your preferred name. Change the condition type to **Numeric**, the test frequency to **On data insertion**, select your channel, enter your condition (for example **"Field 2 (Humidity) is greater than or equal to 60"**), select the just created ThingHTTP and set run to **Only the first time the condition is met**. Like that, you will recieve a notification only once the condition is met until it is no longer met. If you set this on "every time ...", you will recieve notifications every time you insert data until the condition is no longer met. Now finally press "Save". Your humidity-tracker should now perfectly work! To test it, you can set the condition to a value lower than the current value and run the react every time the condiiton is met. If you recieve lots of notifications now, it works perfectly and you can reset the values.

### 7. **Addition**: Two sensors and check for invalid values

Since I have two DHT22 sensors, I adapted the script to measure with both sensors but write the average value into the chart. Additionally, I sometimes got alerts saying the humidity is something like 8000% or the temperature suddenly is something like 1°C or 80°C. Although I only plot the average of the last fifteen values, the react still triggers because one value has been absolutely wrong. To avoid that, I check if the measured value is higher or lower than a certain value. If so, I write the values measure one minute (since I write every 60 seconds) ago. Here is the responding code (you also find it as a python file in the repository):

```python
import thingspeak
import time
import Adafruit_DHT
 
write_key  = 'WRITE_API' #Enter your write api
read_key   = 'READ_API' #Enter your read api
pin1 = RASPBERRY_PI_PIN #Enter the number of the first sensor
pin2 = RASPBERRY_PI_PIN #Enter the number of the second sensor
sensor = Adafruit_DHT.DHT22 #If you´re using the DHT22

# offset last values with values from pin1
lasthumidity, lasttemperature = Adafruit_DHT.read_retry(sensor, pin1)
 
def measure(channel):
    try:
        humidity1, temperature1 = Adafruit_DHT.read_retry(sensor, pin1)
        humidity2, temperature2 = Adafruit_DHT.read_retry(sensor, pin2)

        averagetemperature = (temperature1 + temperature2) / 2
        averagehumidity = (humidity1 + humidity2) / 2

        # if the temp is higher than 50 or lower than 10, the value can not be right
        if (averagetemperature <= 50) & (averagetemperature >= 10): 
            temperature = averagetemperature 
        else:
            temperature = lasttemperature
        # if the humidity is higher than 80 or lower than 20, the value can not be right
        if (averagehumidity <= 80) & (averagehumidity >= 10): 
            humidity = averagehumidity 
        else:
            humidity = lasthumidity

        # write
        response = channel.update({'field1': temperature, 'field2': humidity})
        
        # read
        read = channel.get({})
        print("written")

        # save values 
        lasttemperature = temperature
        lasthumidity = humidity
        
    except:
        print("connection failed")
 
 
if __name__ == "__main__":
    channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
    while True:
        measure(channel)
        time.sleep(60)
```

