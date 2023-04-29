# Purpose

The purpose of this project is to receive data from a Mark-10 force transmitter and send the data over to a PC via
bluetooth. A raspberry pi is used to receive data through a serial connection from the Mark 10, then the test begins and
ends when the user presses the start/stop button. Once the button is pressed to stop the test, the pi sends the force
data to a computer, then the computer stores and shows a plot of the data. There are three lights being controlled with
the following usages:

* Blue Light - This indicates that the raspberry pi is connected to the computer. If flashing, then that means that the
  pi is booting up and is not connected to the server through bluetooth.
* Yellow Light - This indicates that the raspberry pi is receiving data from the Mark 10. If flashing, then that means
  that the pi was booted, but the Mark 10 is not plugged up. The Mark 10 can be powered off at boot up, but it must be
  at least plugged up to get past the boot up stage.
* Green Light - This indicates that the test data is being recorded. If flashing, then that means that the button was
  pressed and the above two lights were not on.

# Installation and Set-Up

## Mark 10

The Mark 10 device must be set to units of either lbF, kgF, or kN. The other units will not work with the compressive
load cell. If other units are used, such as with torque load cells, the unit field in the data files/graphs will be left
blank.

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

The raspberry pi must be connected to Wi-Fi for this initial set-up in order to download the appropriate packages later
on. If there is a high level of difficulty in getting the past IT as in an industrial setting, then consider connecting
to a personal hot spot.

Make sure that `bluez` is installed by typing in the following in the command prompt,

`sudo apt-get install bluez`

This package is necessary for checking a bluetooth connection at the pi's boot-up.

### Wiring

For wiring the pi, refer to the figure below.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/Mark-10-Wiring.png)

The value of the resistors are 330 ohms. The pin numbers shown in the note refer to the board pin numbers as opposed to
the BCM numbering scheme. That is, the board pin numbers refer to the physical layout on the board. Below is a physical
picture for reference.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f4.jpeg)

### Setting Up the Python Environment

First, download all the necessary python scripts from this repository. If not familiar with git, then download and
extract the zipfile by navigating to this position:

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f5.png)

Extracting the zipfile can be done through the pi's file system GUI. Consider placing the project into the desktop.
Next,
run the following commands in the terminal (CTRL+ALT+T) to create a virtual environment.

`cd ~/Desktop/Mark-10-master`

`python3 -m venv venv`

`source venv/bin/activate`

`pip install pyserial RPi.GPIO matplotlib`

Now running `pip list` should output the following,

```angular2html
Package             Version
------------------- -------
contourpy           1.0.7
cycler              0.11.0
fonttools           4.39.3
importlib-resources 5.12.0
kiwisolver          1.4.4
matplotlib          3.7.1
numpy               1.24.3
packaging           23.1
Pillow              9.5.0
pip                 20.3.4
pkg-resources       0.0.0
pyparsing           3.0.9
pyserial            3.5
python-dateutil     2.8.2
RPi.GPIO            0.7.1
setuptools          44.1.1
six                 1.16.0
zipp                3.15.0
```

### Checking the Serial Connection

Making sure the Mark 10 is plugged up, run the following,

`ls /dev | grep tty*`

Toward the bottom of the output, there should be a `ttyUSB0` path. Ensure that this path matches that shown at the top
of the `rpi_main.py` script.

At this point, running the `serial_light_test.py` file should be successful. Make sure that the wiring is completed from
above, and that the virtual environment is activated still (should see "venv" to the left of the current path), and the
Mark 10 is plugged up, then run `python serial_light_test.py` from the terminal. The script will run for about 11
seconds, and pressing the Data button on the Mark 10 should toggle the yellow light on and off.

### Configuring the Pi to Run at Boot-Up

In order to run the software in a state where the raspberry pi is not tethered to a screen or keyboard, the script needs
to be executed at the boot-up of the device. This is done by first modifying the `rpi_bash.sh` script. The script path
in that file needs to be modified. First, run the following,

`nano rpi_bash.sh`

Use the arrow keys to move the cursor and modify the path next to the `cd` command to match the working directory of
the project (`/home/<user name>/Desktop/Mark-10-project`). Note that the path should be in quotes if there are spaces
in the path string. Once finished, press CTRL+X, then "y", then enter. Then run,

`chmod +x rpi_bash.sh` This makes the script executable.

Now to make the script run at boot-up, the `rc.local` file must be modified. Do this by running the following,

`sudo nano /etc/rc.local`

Move the cursor with the arrow keys to a line that is above `exit 0` and below `fi`. Add in

`/bin/bash /home/<user name>/Desktop/Mark-10-master/rpi_bash.sh &`

Press CTRL+X, then "y", then enter. Now running `sudo /etc/rc.local` will run the `rpi_main.py` script, and a blinking
blue light should be observed. If that script executes, then the script will run at boot up. If the blue light begins
flashing, then that means that the pi is not connected to the server through bluetooth. To end the script, the process 
for the `rpi_bash` sequence must be found and terminated. The script is being run in the background, but this can be 
done by running the following,

`ps aux | grep rpi_bash`

Find the process's PID number in the second column, then run

`sudo kill <PID number>`

Additionally, if ever troubleshooting in the future, it is important that the `rpi_main.py` script be ended before
attempting to run it manually. Find the PID sequence by running `ps aux | grep rpi_main` and eliminate it as above.

### Bluetooth Pairing

The raspberry pi needs to be paired to the server computer before being able to run the script. Turn on bluetooth on
both the raspberry pi and the Windows computer. Next, click on Add Device from the raspberry pi's bluetooth settings:

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f6.png)

Select the desired device, then click pair:

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f7.png)

Once initiated, both the raspberry pi and the computer will receive a pop-up like this:

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f8.png)

Click Yes on both of them quickly before the response times out. Next, navigate to the Devices and printers screen:

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f9.png)

Note, a paired device does not mean that the computer is connected. The computer must be in the connected state in order
to successfully execute the scripts. Next, right-click on raspberrypi, then go to the Bluetooth tab and rename the pi to
the desired name.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f10.png)

It may be necessary to restart bluetooth on the computer for the name to update. Ensure that the name here matches the
name at the top of the `rpi_main.py` file.

### Finding the Server's MAC Address

On the computer, open up the command prompt. Making sure bluetooth is turned on, run the following command,

`ipconfig /all`

The computer's MAC address is the physical address under the bluetooth network heading. On the raspberry pi, making sure
that the terminal is still in the working directory, run

`nano rpi_main.py`

Use the arrow keys to move to the `ADDRESS` variable declaration, and change the value of the MAC address to match that
seen from above. Press CTRL+X, then "y", then enter.

## Computer

The computer must have python properly installed. Do this by navigating to
the [python downloads page](https://www.python.org/downloads/). Download the latest installer and run it. In an
industrial setting, IT may have to be involved in order to whitelist running python or the installer. Select custom
installation.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f11.png)

Leave the default optional features checked. Click next. Ensure that the Add Python to environment variables is
selected, and install python in the desired directory. It is recommended that python be stored at the root directory as
shown below.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f12.png)

Click install. Now the installer can be deleted, and running `python --version` in the command prompt should output the
version just installed (assuming there are no other installations of python interfering). If the windows store launches,
then that means that python was not added to the environment variables.

### Setting up the Python Environment

Download the necessary files as done in the raspberry pi set-up. Consider placing the Mark-10-master folder in the 
desktop and navigate to this working directory's position in the command prompt using `cd`. Run the following,

`python -m venv venv`

`venv\Scripts\activate`

`pip install matplotlib`

Open the `server_connection.py` file in Notepad and modify the `ADDRESS` variable to match the address from above. Now
running `python server_connection.py` in the command prompt will launch the server, and it will begin listening for the
raspberry pi. Bluetooth has to be turned on in order for the server to start running.

Next, boot up the raspberry pi. If the blue light starts flashing then that means that the computer did not make the 
connection automatically. Open the bluetooth settings on the computer and connect to the pi. If the Mark 10 is also 
plugged up, the yellow light and the blue light should turn solid, and there should be a message in the server script
indicating a connection. Now pressing the button should begin recording the data and the green light should come on. 
There should be message saying that units have been received. Press the button again to end the test. A plot should 
automatically pop up.

![image not found](https://raw.githubusercontent.com/gabemorris12/Mark-10/master/images/f13.png)

The data gets stored in the working directory to a folder called `data` both locally to the raspberry pi and on the 
computer. To make it easier to run the server, modify the path in the `server.bat` file by right-clicking on it in the 
file manager and pressing edit. Now the file can be moved to the desktop and double-clicking on it will run the server.
Running the batch file, however, may alert anti-malware software. Be sure to whitelist this process, or consult IT if
in an industrial setting.