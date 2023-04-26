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
load cell. If other units are used, such as with torque load cells, the unit field in the data files/graphs will be left
blank. Additionally, **the Mark 10 should be plugged up to the pi before powering on the pi**.

### Configuring the Serial Output
Select the Menu button, then select the Serial/USB Settings option. Ensure that the baudrate is set to 9600. If a value
other than 9600 is desired, then add an argument to the serial object in the `rpi_main.py` file 
(`data = SerialConnection(SERIAL_PORT, baudrate=19200)`) and make sure that the value matches the setting of the Mark 10. 

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f1.png)

Next, make sure that the Mark 10 is sending data through the USB automatically. Select Auto Output, then the Enabled 
button.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f2.png)

Additionally, the Outputs per Sec. value must match the values seen in at the top of the `server_connectin.py` and 
`rpi_main.py` files. Not ensuring this will result in wrong time data.

Press the Data button on the Mark 10 and notice the flashing arrows in the bottom left corner of the main screen. **If
the arrows are not flashing, then the pi will not be able to run a test, and the yellow light will be off.**

## Raspberry Pi
For setting up the OS, [refer to this video](https://youtu.be/1WDagiA8fdU). However, instead of installing the 32-bit
operating system, install the 64-bit operating system shown below.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f3.png)

For wiring the pi, refer to the figure below.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/Mark-10-Wiring.png)

The value of the resistors are 330 ohms. The pin numbers shown in the note refer to the board pin numbers as opposed to
the BCM numbering scheme. That is, the board pin numbers refer to the physical layout on the board. Below is a physical
picture for reference.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f4.jpeg)
