from machine import Pin
import time

led = Pin("LED", Pin.OUT)

def blink_builtin_led_infinity(interval_time: int = 1) -> None:
    while True:           
        led.value(0)
        time.sleep(interval_time)
        led.value(1)
        time.sleep(interval_time)
    return    
