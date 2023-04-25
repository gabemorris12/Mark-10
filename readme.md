# Purpose
The purpose of this project is to receive data from a Mark-10 force transmitter and send the data over to a PC via 
bluetooth. A raspberry pi is used to receive data through a serial connection from the Mark 10, then the test begins and
ends when the user presses the start/stop button. Once the button is pressed to stop the test, the pi sends the force 
data to a computer, then the computer stores and shows a plot of the data. There are three lights being controlled with 
the following usages:

* Blue Light - This indicates that the raspberry pi is connected to the computer.
* Yellow Light - This indicates that the raspberry pi is receiving data from the Mark 10.
* Green Light - This indicates that the test data is being recorded. If flashing, then that means that the pi is booting up, or the button was pressed and the above two lights were not on.

# Installation and Set-Up
## Mark 10
The Mark 10 device must be set to units of either lbF, kgF, or kN. The other units will not work with the compressive 
load cell. Additionally, **the Mark 10 should be plugged up to the pi before powering on the pi**.

### Configuring the Serial Output
Select the Menu button, then select the Serial/USB Settings option. Ensure that the baudrate is set to 9600.

![image not found](https://github.com/gabemorris12/Mark-10/image/f1.png)
