# CraftBeerPi4 PCA9535 IO Actor Plugin 

### PCA9535 based Actor

Plugin will add an PCA9535Actor which has to possibility to define up 8 additional actors to your pi. The board needs to be connected via I2C
Theoretically, multiple boards (up to 8) could be connected with different addresses to make up to 64 IO ports available. However, the plugin supports one board.

### Installation: 
```
sudo pip3 install https://github.com/walidbadar/cbpi4-PCA9535-GPIO/archive/main.zip
sudo python3 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```
### Usage:

- Configure the PCA9535 I2C Address in the cbpi global settings. 
- Add an actor under Hardware/Actor and select PCA9535Actor
- Select the pin you want to switch (9 to 16)
- Select 2 or 5 seconds for the Samplingtime (Will define the 'Resolution' for Power settings)
- Select Inverted yes or no. No means, that the pin will be on high if the sensor is active

Made for a Scientist & Brewer - Tomasz Czernecki, PhD 
Contact: tomasz.czernecki@gmail.com
https://www.linkedin.com/in/tomaszczernecki/
