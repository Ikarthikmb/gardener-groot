# Tracking Essential Features Affecting The Plants Using Raspberry-Pi

> Contents:
> - Introduction
> - Connecting Raspberry Pi
> - Installing Libraries
> - The Code 

---

## Introduction

The plants are like all the other living organisms, they take care of themselves and sometimes dry while unable to help themselves. Someone external has to look after those like a gardener does. This project is built using Raspberry Pi.

The device collects the sensor value from all the inputs and updates the row of  `database-groot.csv` file for every 30 seconds. Alternatively, runs the motions detection code for every 2 seconds, any motion identified will be emailed to the authorised person. All the data is logged to to the file `database-groot.csv` and is emailed before the execution is stopped. 

![All the components used](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2021.34.30.jpg)

**Hardware Components:**

1. Raspberry Pi
2. Pi Camera
3. PIR Motion Sensor
4. Soil Moisture Sensor
5. LDR 
6. DHT11 Temperature and Humidity Sensor
7. Breadboard
8. MCP3008
9. LED's (Red, Blue used here)
10. Jumper wires

**Software and Applications:**

1. Raspbian Buster OS
2. Bitvise SSh Client
3. VNC Viewer


## Connecting Raspberry Pi
 
| ![one](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2021.41.21.jpg)   | ![two](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2022.22.59.jpg)  |
| --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| ![three](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2022.23.42.jpg) | ![four](https://github.com/Ikarthikmb/gardener-groot/blob/master/images/2020-04-14%2022.24.12.jpg) |

Login to Raspberry-pi using ssh or through monitor. If you want to learn how to set up your pi click [here](https://www.instructables.com/id/Set-Up-Raspberry-Pi-4-Through-Laptoppc-Using-Ether/).

 Make the necessary connections from the circuit diagram, power up the pi. Here I've connected the raspberry through wi-fi network and opened it through VNC-Viewer.

 Open the terminal and dowload this repository to do so 

    sudo apt-get install updates
    sudo apt-get install full-upgrade
    git clone https://github.com/Ikarthikmb/gardener-groot


## Installing the Libraries

1. Adafruit MCP3008

To install from the source on Github connect to a terminal on the Raspberry Pi and run the following commands:

You should see the library install succeed and finish with a message similar to the following:

    sudo apt-get install build-essential python-dev python-smbus git
    cd ~
    git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
    cd Adafruit_Python_MCP3008
    sudo python setup.py install

If you see an error go back and carefully check all the previous commands were run, and that they didn't fail with an error.

2. Adafruit Python DHT Sensor Library

Using  `pip` to install from PyPI.

    sudo pip install Adafruit_DHT

3. SMPTLIB

using `pip` install

    pip install secure-smtplib

## The Code

Now to run the code open the terminal go through the following steps:

    cd gardener-groot
    python grootv1.py