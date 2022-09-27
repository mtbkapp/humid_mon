import humid_mon
import machine
import time

def log_ex(ex):
    f = open("error.txt", "w")
    f.write("{0}\n".format(ex))
    f.close()

led = machine.Pin("LED", machine.Pin.OUT)

try: 
    humid_mon.kick_loop()
except Exception as ex:
    log_ex(ex)
    while True:
        led.on()
        time.sleep_ms(100)
        led.off()
        time.sleep_ms(100)

