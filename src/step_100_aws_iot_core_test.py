#!/usr/bin/python3

# Import SDK packages
import datetime
import json
import random
import time

from AWSIoTPythonSDK.exception.AWSIoTExceptions import connectTimeoutException
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#MQTT client parameters
MQTT_CLIENT_ID = #einen Namen für den Client vergeben
MQTT_HOST = #den MQTT host 
MQTT_TOPIC = #einen Namen für den Channel 

#Certificate files
CERT_FILE_PATH = #das Verzeichnis in dem die Zertifikate liegen 
CA_ROOT_CERT_FILE = "AmazonRootCA1.pem"
THING_CERT_FILE = # die cert-Datei des Things 
THING_PRIVATE_KEY = # der Private Key des Things 

def create_mqtt_client():
    ''' This function creates and configures the MQTT client
        using the parameters given above'''

    mqtt_client = AWSIoTMQTTClient(MQTT_CLIENT_ID)
    mqtt_client.configureEndpoint(MQTT_HOST, 8883)
    mqtt_client.configureCredentials(CERT_FILE_PATH + CA_ROOT_CERT_FILE, CERT_FILE_PATH + THING_PRIVATE_KEY, CERT_FILE_PATH + THING_CERT_FILE)
    
    mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
    mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
    mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

    return mqtt_client


def publish_sample_data(mqtt_client, sequence_nr):
    ''' This function generates some random data and sends it to the 
        AWS IoT Core.'''
    message = {}
    message['timestamp'] = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    message['temperature'] = random.randint(0,30)
    message['humidity'] = random.randint(0,100)
    messageJson = json.dumps(message)
    mqtt_client.publish(MQTT_TOPIC, messageJson, 0)

    
if __name__ == "__main__":
    mqtt_client = create_mqtt_client()

    try:
        if mqtt_client.connect():
            count = 0
            while True:
                publish_sample_data(mqtt_client, count)
                time.sleep(2)
                count += 1

    except connectTimeoutException as e:
        print(e.message)
