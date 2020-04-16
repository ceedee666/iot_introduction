import network
import ntptime


def connect_wifi():
    wifi_passwds = {}

    with open("/cert/wifi_passwds.txt") as f:
        for line in f.readlines():
            wifi_id, passwd = line.split(":")
            wifi_passwds[wifi_id] = passwd

    wlan = network.WLAN(network.STA_IF)

    if not wlan.isconnected():
        wlan.active(True)

        visible_wifis = [str(w[0]) for w in wlan.scan()]
        known_wifis = list(filter(lambda w: w in wifi_passwds.keys(), visible_wifis))

        if len(known_wifis) > 0:
            wifi = known_wifis[0]
            print('connecting to network', wifi)
            wlan.connect(wifi, wifi_passwds[wifi])
            while not wlan.isconnected():
                pass

            print("connected:", wlan.ifconfig())
        else:
            print('No known network available.')


def synchronize_rtc():
    # set the rtc datetime from the remote server
    ntptime.settime()
