# CraftBeerPi4 PCF8574 IO Actor Plugin 

### PCF8574 based Actor

Plugin will add an PCF8574Actor which has to possibility to define up 8 additional actors to your pi. The board needs to be connected via I2C
Theoretically, multiple boards (up to 8) could be connected with different addresses to make up to 64 IO ports available. However, the pulgin supports one board.

### Installation: 
- sudo pip3 install cbpi4-PCF8574-GPIO
- or install from repo: sudo pip3 install https://github.com/avollkopf/cbpi4-PCF8574-GPIO/archive/main.zip
- cbpi add cbpi4-PCF8574-GPIO
	
### Usage:

- Add an actor and select PCF8574Actor
- Select a pin you want to switch
- Select 2 or 5 seconds for the Samplingtime (Will define the 'Resolution' for Power settings)
- Select Inverted yes or no. No means, that the pin will be on high if the sensor is active


### Hardware requirements:

Some information can be found here: https://www.instructables.com/PCF8574-GPIO-Extender-With-Arduino-and-NodeMCU/
Connect the device to 5 Volt, GND and your I2C bus. Check the Address ans set it to a different address if required
According to the datasheet, the pins can handle up to 25 mA. If you want to trigger an SSR or a relais, it is recommended to add a darlington array like the ULN2308

### Changelog:

- 09-12-21: (0.0.1) Initil releasa
