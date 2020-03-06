import network

WIFI_SSID = "iPhone"
WIFI_PW = "123Qwerty"

wlan = network.WLAN(network.STA_IF)

if not wlan.isconnected():
    wlan.active(True)
    print('connecting to network', WIFI_SSID)
    wlan.connect(WIFI_SSID, WIFI_PW)
    while not wlan.isconnected():
        pass

print("connected:", wlan.ifconfig())

