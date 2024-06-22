import network
import time

def connectWiFi(ssid: str, password: str) -> bool:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
        
    # Handle connection error
    if wlan.status() != 3:
        msg = 'network connection failed'
        res = False
        raise RuntimeError(msg)
    else:
        print(f'Connected\nip = {wlan.ifconfig()[0]}')
        res = True
    
    return res

if __name__ == "__main__":
    import private
    import test
    ssid = private.ssid
    password = private.password
    res = connectWiFi(ssid, password)
    if res:
        test.blink_builtin_led_infinity(0.1)


