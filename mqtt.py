from umqtt.robust import MQTTClient

# The certificate and key file need to be converted from PEM to DER format first
#
# $ openssl x509 -in aaaaaaaaa-certificate.pem.crt.txt -out cert.der -outform DER
# $ openssl rsa -in aaaaaaaaaa-private.pem.key -out private.der -outform DER

CERT_FILE = "/cert/cert.der"
KEY_FILE = "/cert/private.der"
MQTT_CLIENT_ID = "my_d1_mini"
MQTT_PORT = 8883

MQTT_HOST = "a1lo9dnpk3t0qk-ats.iot.eu-central-1.amazonaws.com"


def connect_mqtt():
    with open(KEY_FILE, "r") as f:
        key = f.read()

    with open(CERT_FILE, "r") as f:
        cert = f.read()

    ssl_params = {"cert": cert, "key": key, "server_side": False}
    mqtt_client = MQTTClient(
        client_id=MQTT_CLIENT_ID,
        server=MQTT_HOST,
        port=MQTT_PORT,
        keepalive=5000,
        ssl=True,
        ssl_params=ssl_params,
    )

    mqtt_client.connect()

    return mqtt_client
