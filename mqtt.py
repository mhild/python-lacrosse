import paho.mqtt.client as mqtt
import json
import os

import time
from datetime import datetime


from icecream import ic
import socket

HOSTNAME = os.environ.get("RPI_UID", socket.gethostname())


BROKER_HOST = os.environ.get("MQTT_BROKER_HOST", "127.0.0.1")
BROKER_PORT = os.environ.get("MQTT_BROKER_PORT", 1883)

try:
    BROKER_PORT = int(BROKER_PORT)
except ValueError:
    ic('Invalid Port specification ', BROKER_PORT)
    ic('defaulting to 1883')
    BROKER_PORT = 1883
    
BASE_TOPIC = 'jeelink'


def get_sensor_cfg(name, type, unit, icon=None, device_class=None):
    cfg = { 
        "unit_of_measurement": f'{unit}',
        "value_template": "{{{{ value_json.{type} }}}}".format(type=type),
        "state_topic": f"{BASE_TOPIC}/{name}/state",
        "name": f"{type}",
        "unique_id": f"jeelink_{name}_{type}",
        "device": {
            "identifiers": [
                f"jeelink_{name}",
            ],
            "name": f"{name}",
            "model": f"jeelink",
            "manufacturer": "Jeelink"
        }
    }
    
    if icon is not None:
        cfg['icon'] = icon
    if device_class is not None:
        cfg['device_class'] = f"{device_class}"
        
    return json.dumps(cfg, indent=2)
    
    
MEASUREMENT_LIST = [
    {'type':'temperature', 'unit' : '°C', 'icon': None, 'device_class': 'temperature' },
    {'type':'humidity', 'unit' : '%', 'icon': None, 'device_class': 'humidity' }, 
    ]

def send_auto_discovery_messages(name):
    for m in MEASUREMENT_LIST:
        msg = get_sensor_cfg(name, m['type'], m['unit'], m['icon'], m['device_class'])
        
        topic = f"homeassistant/sensor/{m['type']}_{name}/config"
        send(topic, msg, retain=True)
        
    
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, f"jeelink_mqtt_bridge_{HOSTNAME}")

REGISTERED_SENSORS = []

def send_message(name, message):
    
    if name not in REGISTERED_SENSORS:
        send_auto_discovery_messages(name)
        REGISTERED_SENSORS.append(name)
    topic = f"{BASE_TOPIC}/{name}/state"
    send(topic, message)
    
def send(topic, payload, retain=False):
    global client
    if not client.is_connected():
        ic('connecting to broker:', BROKER_HOST, BROKER_PORT)
        client.connect(BROKER_HOST, BROKER_PORT, 60)  
    result:mqtt.MQTTMessageInfo = client.publish(topic, payload, retain)
    client.loop_start()
    

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f'{datetime.now()} Publish: successful')
        print(f'payload: \n{json.dumps(payload, indent=2)}')
        last_publish = time.time()

    else:
        print(f'{datetime.now()} Publish: failed {result}')
    
