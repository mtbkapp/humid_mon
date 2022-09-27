# humid_mon
Uses a Raspberry PI Pico W with a Pimoroni BME 680 to push temperature and 
humidity readings to Prometheus and Grafana.

## Run Grafana and Prometheus
1. Install docker
2. run `docker-compose up -d` from 

## Install on the Pico W
1. Flash the attached Pimoroni MicroPython library to the PI (pimoroni-picow-v1.19.6-micropython.uf2).
2. Update the `humid_mon.py` file with the address to the machine running Prometheus and Grafana.
2. Update the secrets.py file with the correct wifi ssid and password.
3. Use rshell to copy all the python code to the pico.


## Run the Pico W
After the Pico is flashed with Pimoroni's MicroPython and the Python code just 
add power and it should run. When the Pico is taking a reading and pushing
the data the LED will be on. If the LED is blinking rapidly an Exception was
raised. Use rshell to check the contents of the `error.txt` file for the 
exception message.


### Misc
Not in anyway related to the amazing [Vulfmon](https://www.youtube.com/watch?v=0k2dGhF6yVk).
