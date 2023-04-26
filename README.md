# autobox name under construction
This is code to run an automated grow box or room. It was created with the intent of controlling the climate of a small area. It hasn't been tested yet and should not be expected to work as intended until we have been able to test it extensively. 

It's operation uses a microcomputer capable of running python code, such as a Raspberry Pi or alternative. It needs to have GPIO pins installed for I/O signals. 

It uses a sensor, a relay module, and some basic python code. The exact specifications and necessary python modules are laid out below.

# Instruction
## Purchasing list
### Microcomputer
- Microcomputer capable of internet with Python and GPIO pins installed.

### Sensor
- Sensor capable of Temp and Humidity and I2C communications. 
    - Relative Humidity should be able to read above 80%. Most cheap ones don't have this capacty. 
    
    - This project uses : https://www.amazon.com/Adafruit-BME280-Temperature-Humidity-Pressure/dp/B013W1AJUY
### Jumpers 
-Set of breadboard jumpers. 
    - Need at least 10 jumpers. They can all be female-to-male if you want to run through a breadboard, or:
        - 4 female-male, 6 female-female
### Relays
- 4 relay module
    - We have this one: https://www.amazon.com/dp/B00E0NSORY?psc=1&ref=ppx_yo2ov_dt_b_product_details
- It is important to get a relay module and not just use loose relays. Unless you are confident in your electronics hobby capabilities, it is very easy to cause a short and ruin your computer, relay, or hurt yourself.
- Power supply capable of 5v and 400mA

### Externals
- The necessary items to control the climate in your space
- We are using a heater, cooler, and humidifier
- THESE RELAYS ARE ONLY SUITABLE TO UP TO 10 AMPS. CHECK YOUR AMPERAGE ON YOUR DEVICES. A/C UNITS AND LARGE HEATERS OFTEN GO ABOVE THAT EASILY.

# Installation

## Prep the Pi
- Prep your pi and set it up for SSH. 
    - If you don't know how to do SSH, google it. It isn't required, but it's sure a lot easier to set up and interact with your pi this way.
    - Make sure your pi is set to accept i2c communications. If you don't know how to do this, google it for your specific pi.
    - Ensure pip and python are updated
- Download the following modules:
    - The adafruit BME280 sensor library avaiable here: https://github.com/adafruit/Adafruit_CircuitPython_BME280
        ```
        sudo pip3 install adafruit-circuitpython-bme280
        ```
    - matplotlib 
        ```
        sudo apt-get install python3-matplotlib
        ```
    - The python discord bot library. 
        - documentation: https://discordpy.readthedocs.io/en/stable/intro.html
        ```
        pip3 install discord
        ```
    - The python Pandas library
        - documentation: https://pandas.pydata.org/docs/getting_started/install.html
        ```
        pip3 install pandas
        ```  
  
- Once all the modules are downloaded, install the BME280 sensor to the GPIO pins according to the manual. Each pi often has different GPIO setting outputs, so make sure yours is the correct one.
- Make a directory in root called "data." This is currently a very jank fix for something that we plan on fixing soon, but as for now, this is where the data is stored as its saved.
- Follow the instructions to set up your bot and get a token for it. Save it to a text file in root called "token.txt"
- Download the autobox code into your root.

## Sensor
- The sensor should be automatic once it's hooked into the pi. Just make sure it's installed correctly, fire and forget.

## Relays
- The relay will need a seperate power supply, as the volts and amps the pi is capable of isn't enough for the relay.
- The relay's soldered pins can also shock you if you aren't careful. We recommend 3D-printing this file: https://www.thingiverse.com/thing:957292 or finding some protective shielding. It's easy to avoid touching the pins, but it's also very easy to get shocked.
- Find which GPIO pins you wish to connect and use the female-to-female jumpers to install each IN#. 
- Record which pins you are using and set them in the settings.JSON in the autobox/controller/settings.JSON.
- You can now wire your relays. If you don't know how to do this, I recommend watching some videos.
    - Basically, relays work as a switch that complete a circuit. All you have to do is cut one side of the power cable and feed it through the relay. 
    - READ THE MANUAL ON RELAYS. IMPROPER INSTALLATION CAN LEAD TO SERIOUS PROBLEMS.
    - INSTALL USING THE 'ALWAYS OPEN' SIDE.

## Bot Set-up
- visit discord.com/developers
- click on applications
- click new application
- go to the bot tab and click 'add bot'
- from this page you can copy the token that will be used to write the code for your bot
- scroll down and enable all 'priveleged gateway intents'
- go to OAuth2 --> URL Generator
- under scopes, select bot
- under bot permissions, select 'Read Messages/View Channels', 'Send Messages' and 'Attach Files'
- copy and paste the link into your browser, this will prompt you with questions regarding permissions you want the bot to have in the server. Select the same permissions as the previous step. The bot should now be added to the server.
- In discord, go to settings --> advanced and activate Developer Mode

## Settings Setup
- The settings are located in picode/controller/settings.json, this is where you will input all of the information specific to your system and setup
- Thresholds:
    - LL: The temp at which you would like the system to alert you that the temp is too low
    - HON: The temp at which you would like the heater to turn on
    - HOFF: The temp at which you would like the heater to turn off
    - CON: temp at which to turn the cooler on
    - COFF: temp at which to turn the cooler off
    - HUMON: humidity level at which to turn the humidifier on
    - HUMOFF: humidity level at which to turn the humidifier off
    - HHUM: High humidity at which an alert should be sent
    - HH: High-High, the high temp at which an alert should be sent
- GPIO_Pins:
    - each of these should be the physical pin # associated with the named pin
- Token_Paths:
    - pi_path: the path to the bot_token.txt file on your pi or alternative device
    - test_path: there are 4 test_path variables preset, each of these should consist of the respective paths to the bot_token.txt file on every contributors       personal machine. To add more test_path variables, simply add another value in the Token_Paths dictionary with the naming convention: test_path_n where       n is the number of test_path variables (starting at 0).
- Channel_Id: 
    - The channel id should be input as an int, with no quotations. 
    - The channel ID can be obtained by right clicking on the desired channel within discord, and clicking "Copy Channel ID"
   
## Relay and Sensor Testing
- Before running the main program, you should run relay_test.py and sensor_test.py to make sure the relays and the sensor are working properly. 
- Relay Testing:
    - The relay test will turn each relay on for 5 seconds, then turn it off. As it is doing so, it will print which pin it is currently testing to the             console. To run the test again, simply run the file again. 
- Sensor Testing: 
    - The sensor test will print to the console the current temperature and humidity a total of 30 times or until interuppted by the keyboard. 
  
## Final steps
- Go into settings and ensure your GPIO pins are set, and make sure the values for thresholds are where you want them. 
- Navigate into the Autobox directory and use `sudo python start.py'. This will begin all processes. Hope it works!
   
        
