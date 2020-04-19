# Tracking Essential Features Affecting The Plants Using Raspberry-Pi

# Contents:

- [Tracking Essential Features Affecting The Plants Using Raspberry-Pi](#tracking-essential-features-affecting-the-plants-using-raspberry-pi)
- [Contents:](#contents)
  - [Introduction](#introduction)
  - [Connecting Raspberry Pi](#connecting-raspberry-pi)
  - [Installing the Libraries](#installing-the-libraries)
  - [The Code](#the-code)
  - [Analysing Data](#analysing-data)
  - [Conclusion](#conclusion)
  - [Resources](#resources)

---

## [Introduction](#contents)

| ![three](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2022.23.42.jpg) |
| --------------------------------------------------------------------------------------------------- |


The plants are like all the other living organisms, they take care of themselves and sometimes dry while unable to help themselves. Someone external has to look after those like a gardener does. This project is built using Raspberry Pi.

The device collects the sensor value from all the inputs and updates the row of `database-groot.csv` file for every 30 seconds. Alternatively, runs the motions detection code for every 2 seconds, any motion identified will be emailed to the authorised person. All the data is logged to to the file named `database-groot.csv` and is emailed for every hour and also when the execution is stopped.

**Hardware Components:**

| ![All the components used](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2021.34.30.jpg) |
| --------------------------------------------------------------------------------------------------------------------- |


1. Raspberry Pi
2. Pi Camera
3. PIR Motion Sensor
4. Soil Moisture Sensor
5. LDR
6. DHT11 Temperature and Humidity Sensor
7. Breadboard
8. MCP3008
9. LED's (Red, Blue are used here)
10. Jumper wires

**Software and Applications:**

1. Raspbian Buster OS
2. Bitvise SSh Client
3. VNC Viewer

## [Connecting Raspberry Pi](#contents)

| ![circuit connections](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/circuit-connections.png) |
| --------------------------------------------------------------------------------------------------------------- |


**The Circuit Connections:**

- Moisture Sensor
  - Center pin connected to channel-0 of MCP3008 IC
  - One side pin to VCC(+3V)
  - Other side pin to GND
- Temperature & Humidity
  - DATA pin connectedd to Raspberry-pi pin 4 in BCM mode
  - VCC pin connected to +3V
  - GND pin connected to GND
- PIR
  - DATA pin connected to pin 17 of Raspberry-pi in BCM mode
  - VCC pin connected to +5V
  - GND pin connected to GND
- LDR
  - DATA pin connected to channel-1 of MCP3008
  - VCC pin cconnected to +3V
  - GND pin connected to GND
- MCP3008
  - MCP3008 DGND to GND
  - MCP3008 CS to RPI4 8
  - MCP3008 DIN to RPI4 10
  - MCP3008 DOUT to RPI4 9
  - MCP3008 CLK to RPI4 11
  - MCP3008 AGND to GND
  - MCP3008 VREFF to +3V
  - MCP3008 VCC to +3

| ![one](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2021.41.21.jpg)     | ![two](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2022.22.59.jpg)  | ![soil](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2022.24.35.jpg)  |
| ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| ![mcp3008](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2022.22.20.jpg) | ![four](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2022.24.12.jpg) | ![final](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2022.20.43.jpg) |

Make the necessary connections from the circuit diagram, power up the pi. Here I've connected the raspberry through wi-fi network and opened it through VNC-Viewer.

Login to Raspberry-pi using ssh or through monitor. If you want to learn how to set up your pi click [here](https://www.instructables.com/id/Set-Up-Raspberry-Pi-4-Through-Laptoppc-Using-Ether/). Assuming you have logged into the Raspberry

Open the terminal and dowload this repository, alternatively follow

    sudo apt-get install updates
    sudo apt-get install full-upgrade
    git clone https://github.com/Ikarthikmb/gardener-groot

You should be able to see the folder `gardener-groot` in the home.

## [Installing the Libraries](#contents)

**1. Adafruit MCP3008**

This library is for setting up the IC MCP3008.

To install from the source on Github connect to a terminal on the Raspberry Pi and run the following commands:

You should see the library install succeed and finish with a message similar to the following:

    sudo apt-get install build-essential python-dev python-smbus git
    cd ~
    git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
    cd Adafruit_Python_MCP3008
    sudo python setup.py install

If you see an error go back and carefully check all the previous commands were run, and that they didn't fail with an error.

**2. Adafruit Python DHT Sensor Library**

Using this library you can read the analog values of _Temperature_ and _Pressure_ into your Raspberry Pi. In terminal

    sudo pip install Adafruit_DHT

**3. smptlib**

This library installs the required packages to send and receive the mails. To install

    pip install secure-smtplib

**4. Pi Camera**

The Picamera library is prebuilt but it is not activated. In order to turn it on

        sudo raspi-config

In the **Menubox** go to `Interfacing` --> `Camera` and then select `Yes` and save. If this is the first time you are turning the camera **ON**, it is recommended to _reboot_ the Pi.

## [The Code](#contents)

| ![output file 01](https://raw.githubusercontent.com/Ikarthikmb/gardener-groot/master/Log_Report_GG/Log%2019-04/images%2019-04/in_op_log_1904.bmp) | ![output file 02](https://raw.githubusercontent.com/Ikarthikmb/gardener-groot/master/Log_Report_GG/Log%2019-04/images%2019-04/ls_op_log_1904.bmp) |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Running the code file `grootv1.py`                                                                                                                | End of the output                                                                                                                                 |

Now to run the code open the terminal go through the following steps:

    cd gardener-groot
    python grootv1.py

You shoud abe able to see the code started, displaying the readings of the sensors. Try touching to plant to test whether the device is cable to capture it. The one problem we faced here is that the the device captures the image for the detected motion even though the plant is not harmed externally.

| ![image capture 01](https://github.com/Ikarthikmb/gardener-groot/blob/master/Log_Report_GG/Log%2019-04/images%2019-04/image-Sun-Apr-19-101919-2020.png) | ![image capture 02](https://github.com/Ikarthikmb/gardener-groot/blob/master/Log_Report_GG/Log%2019-04/images%2019-04/image-Sun-Apr-19-110417-2020.png) |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Image showing a person touching the plant                                                                                                               | Image captured when motion is been detected but not harming the plant                                                                                   |

For detailed log for the day 19 April 2020 click [here](https://github.com/Ikarthikmb/gardener-groot/blob/master/Log_Report_GG/Log%2019-04/OP-grootv1.pdf).

## [Analysing Data](#contents)

| ![The Overall Graph](https://github.com/Ikarthikmb/gardener-groot/blob/master/Log_Report_GG/Log%2019-04/images%2019-04/Temperature%2C%20Humidity%2C%20LightVal%20and%20MoistureVal.png) |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A relation between Temperature, Humidity, LightVal and MoistureVal with respect to time                                                                                                 |

The detailed log of the readings from the Raspberry is sent to the respective email at the end of the code, also it is automatically sent to _email_ for every one hour(Can be customised).

Here in this stage one can apply programming knowledge to _analyse_ and get the results like the waveform and grahs. To make it simpler I used google spreadsheets to analyse and depict a graph for the values obtained. You can take a look oh how the google spreadsheets have given such beautiful layouts.

| ![mvd](https://github.com/Ikarthikmb/gardener-groot/blob/master/Log_Report_GG/Log%2019-04/images%2019-04/MoistureVal%20vs.%20DateTime.png) | ![tvd](https://github.com/Ikarthikmb/gardener-groot/blob/master/Log_Report_GG/Log%2019-04/images%2019-04/Temperature%20vs.%20DateTime.png) |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| ![hvd](https://github.com/Ikarthikmb/gardener-groot/blob/master/Log_Report_GG/Log%2019-04/images%2019-04/Humidity%20vs.%20DateTime.png)    | ![lvd](https://github.com/Ikarthikmb/gardener-groot/blob/master/Log_Report_GG/Log%2019-04/images%2019-04/LightVal%20vs.%20DateTime.png)    |

## [Conclusion](#contents)

After analysing the data it is observed that the _moisture_ in the soil is perfectly alright, the sunlight is varying from high to low which means the light is not properly available to the plant. The _temperature_ is too high for such a plant to survive which means I have to shift the location of the plant immediately to a better place. With the constant high temperature of 32 C the humidity has been decreasing slightly and reached a minimum of 41 percentage.

The final statement is that the location where I'm staying isn't suitable for any plant to grow, infact for me too so, I'm leaving now in search for a better house where myself along with my pot can stay healthy.

---

## [Resources:](#contents)

- [Setting up the Raspberry Pi 4](https://www.instructables.com/id/Set-Up-Raspberry-Pi-4-Through-Laptoppc-Using-Ether/)
- [Wiring and working with MCP3008](https://www.instructables.com/id/Measuring-Soil-Moisture-Using-Raspberry-Pi/)
- [Connecting the Pi camera to Raspberry Pi](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
- [Measuring soil moisture using Raspberry Pi](https://www.instructables.com/id/Measuring-Soil-Moisture-Using-Raspberry-Pi/)
- [How to Set Up the DHT11 Humidity Sensor on the Raspberry Pi](https://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/)
- [Graph of Temperature, Humidity, LightVal and MoistureVal](https://docs.google.com/spreadsheets/d/e/2PACX-1vTuSa28HAoZzqSf02eFfmrphdf843vcm1suHe8Xjd6a1-kv2Clv6b9aIPoK7PJFDjSHAAzVVjkL23uN/pubchart?oid=1268827840&format=interactive)

---
