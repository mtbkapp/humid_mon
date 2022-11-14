# humid_mon.py
#
# Sensor reading portion was adapted from https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/breakout_bme68x/bme68x_demo.py
# Board is BME680 which carries the Bosch BME680 sensor

import machine
import network
import time
import urequests

from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
from pimoroni_i2c import PimoroniI2C


SENSOR_PINS = {"sda": 0, "scl": 1}
POLL_ITERVAL_MS = 60000
    
led = machine.Pin("LED", machine.Pin.OUT)

# import wifi creds from secrets.py
try:
    from secrets import WIFI_SSID, WIFI_PASS, IO_USERNAME, IO_KEY
except ImportError:
    WIFI_SSID = None
    WIFI_PASS = None

ADAFRUIT_URL = "https://io.adafruit.com/api/v2/{0}/feeds/{1}/data"

def init_network_with_retries(wlan, retries):
    print("Attempting to connect. Retries left {0} \n".format(retries))
    if (retries <= 0):
        raise Exception("Out of connect retries")

    wlan.connect(WIFI_SSID, WIFI_PASS)
    init_network_status_check(wlan, retries, 5)


def init_network_status_check(wlan, connect_retries, wait_retries):
    if (wait_retries <= 0):
        raise Exception("Can't wait any longer")
    
    time.sleep_ms(3000)
    status = wlan.status()

    if status == network.STAT_CONNECTING:
        init_network_status_check(wlan, connect_retries, wait_retries - 1)
    elif status == network.STAT_CONNECT_FAIL:
        init_network_with_retries(wlan, connect_retries - 1)
    elif status == network.STAT_GOT_IP:
        if not wlan.isconnected():
            time.sleep_ms(5000)
        if not wlan.isconnected():
            raise Exception("wlan: not connected but got ip? WAT!")
        return
    elif status == network.STAT_IDLE:
        raise Exception("wlan: status is STAT_IDLE!")
    elif status == network.STAT_NO_AP_FOUND:
        raise Exception("wlan: AP not found, ssid = {0}".format(WIFI_SSID))
    elif status == network.STAT_WRONG_PASSWORD:
        raise Exception("wlan: Incorrect password")
    elif status == 2:
        print("unknown status 2, try reconnecting again") 
        init_network_with_retries(wlan, connect_retries - 1)
    else:
        raise Exception("Unknown status {0}".format(status))


def init_network():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    init_network_with_retries(wlan, 5)
    return wlan


def init_sensor():
    i2c = PimoroniI2C(**SENSOR_PINS)
    return BreakoutBME68X(i2c)


def poll_sensor(sensor):
    temperature, pressure, humidity, gas, status, _, _ = sensor.read()
    heater_status = 1 if status & STATUS_HEATER_STABLE else 0 
    return {"temperature": temperature, "humidity": humidity, "heater_is_stable": heater_status}


def encode_metrics(metrics):
    s = ""
    for k, v in metrics.items():
        s = s + k + " " + str(v) + "\n"
    return s

def adafruit_url(feed_id):
    return ADAFRUIT_URL.format(IO_USERNAME, feed_id)

def send_metric(feed_id, v):
    print("Sending metric to feed: {0}".format(feed_id))
    json = {"value": str(v)}
    headers = {"X-AIO-Key": IO_KEY}
    resp = urequests.post(adafruit_url(feed_id), json=json, headers=headers)
    print("Sent, status code = " + str(resp.status_code))
    print(resp.content)
    resp.close()


def c_to_f(c):
    return ((9 * c) / 5) + 32 


def push_metrics(metrics):
    send_metric("temp", c_to_f(metrics["temperature"]))
    send_metric("humidity", metrics["humidity"])
  

def kick_loop():
    print("START")
    print("Connecting to wifi...")
    wlan = init_network()
    print("Connected to wifi.")
    print("Init sensor...")
    sensor = init_sensor() 
    print("Sensor init'd")
    print("Starting poll loop")
    while True:
        if not wlan.isconnected():
            init_network_with_retries(wlan)
        led.on()
        print("Polling sensor")
        metrics = poll_sensor(sensor)
        print("Done polling sensor")
        print("Pushing metrics")
        try:
            push_metrics(metrics)
        except Exception as ex:
            print("Exception pushing metrics", ex)
        print("Done pusihing metrics")
        print("Waiting for next poll")
        led.off()
        time.sleep_ms(POLL_ITERVAL_MS)


