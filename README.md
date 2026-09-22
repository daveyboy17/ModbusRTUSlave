# Modbus RTU Slave Simulator

I needed to test a Modbus RTU master device but all the slave simulators I found were either Windows only or unsuitable.

So, I asked ChatGPT to:
'Write an engineering app for windows and linux in python3 to open a serial port and act as a Modbus RTU slave device.
The Modbus device address should be settable along with input and holding register numbers and the values they contain.
Default baud-rate should be 9600, no parity, one stop bit.'

It has evolved somewhat from Chad's initial offering.

**It is available here under the MIT license.**
Latest version is in the Milestone 3 branch.

## To Run
Install dependencies:
  `pip install -r requirements.txt`
  
Run:
  `python main.py`
  
OR
  `.venv/bin/python3 main.py`


## Cross-platform Deployment

### Windows
  `ModbusSlave.exe`

Created by
  `pyinstaller --onefile --windowed main.py --name ModbusSlave` 

### Linux
  `./ModbusSlave`

Created by:
  `pyinstaller --onefile main.py --name ModbusSlave`
  
Or
  `.venv/bin/pyinstaller --onefile main.py --name ModbusSlave`
  
From a single codebase.


## Using it
The app allows you to add holding registers (numbered 40001...) and input registers (numbered 30001...) and set values for each.
You can also provide names and descriptions for the registers for your own reference.
It should save and reload configurations but it's a little reluctant to do so at present!
You can set the slave address as well as baud-rate etc. and lets you choose a serial port from those available on the system.

When a Modbus message is received it is shown in the main window along with it's decode if the slave address matches.

On the right hand side is a statistics panel that shows bytes, messages, errors, response time and such.

At the bottom is a panel for fault injection like corrupt CRC values, delayed responses, dropped responses, and exceptions.
These settings are read when serial connects so if you want to change them, disconnect and reconnect so they take effect.


## TODO
* Get configuration save and restore to work.
* Add test scenarios to the configuration files - via named files.
* Get error injection to update on the fly.
* Improve the packet monitor and maybe spool it to a logfile as well.
* Separate the GUI from the controls.
