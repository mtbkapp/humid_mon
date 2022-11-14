# humid_mon
Uses a Raspberry PI Pico W with a Pimoroni BME 680 to push temperature and 
humidity readings [Adafruit IO](io.adafruit.com)

## Install on the Pico W
1. Flash the attached Pimoroni MicroPython library to the PI Pico W (pimoroni-picow-v1.19.6-micropython.uf2).
2. Update the secrets.py file with the correct wifi ssid and password.
3. Update the secrets.py file with the io.adafruit.com username and api key.
4. Use rshell to copy all the python code to the pico.


## Run the Pico W
After the Pico W is flashed with Pimoroni's MicroPython and the Python code just 
add power and it should run. When the Pico W is taking a reading and pushing
the data the LED will be on. If the LED is blinking rapidly an Exception was
raised. Use rshell to check the contents of the `error.txt` file for the 
exception message. Exceptions when pushing metrics are ignored.


### [rshell](https://pypi.org/project/rshell/)
* Start: `% rshell`
* Copy file: `rshell> cp humid_mon.py /pyboard/humid_mon.py`
* Start repl: `rshell> repl`
* Start program from repl: `CTRL-D`
* Stop from program from repl: `CTRL-C`
* Exit repl: `CTRL-X`
* Exit rshell: `CTRL-D`


### Misc
Not in anyway related to the amazing [Vulfmon](https://www.youtube.com/watch?v=0k2dGhF6yVk).
