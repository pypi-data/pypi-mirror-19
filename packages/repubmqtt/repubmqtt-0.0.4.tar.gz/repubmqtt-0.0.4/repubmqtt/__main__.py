import paho.mqtt.client as mqtt
import repubmqtt
import json
import sys


DBG = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if DBG: print("Connected with result code "+str(rc))

    for topic in client.topics:
        client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if DBG: print("%s  %s" % (msg.topic, msg.payload))

    try:
        jrecord = json.loads(msg.payload.decode('utf-8')
)
    except Exception as e:
        jrecord = {'rawvalue': msg.payload }
        if DBG: print("payload not json '%s':  %s" %(e, msg.topic+" "+str(msg.payload)))
    jrecord['topic'] = msg.topic
    client.repub.process_message(jrecord)

#
# 
REQUIRED_NAMES = ['MQTT_SERVER', 'MQTT_PORT', 'MQTT_CLIENT_ID', 'MQTT_USERNAME', 'MQTT_PASSWORD',
     'TOPICS', 'RULES', 'xlate']

def main():
    global DBG
    if len(sys.argv) != 2:
        print("usage: %s <conffile>")
        return 1

    conffile = sys.argv[1]
    namespace = {}
    namespace['DBG'] = DBG
    try:
        exec(open(conffile).read(), namespace )
    except Exception as e:
        print("Load of config failed: %s" % e)
        return(1)
    
    err = False
    for name in REQUIRED_NAMES: 
        if not name in namespace:
            print("required entry '%s' missing in config file '%s'" % (name, conffile))
            err = True
    if err:
        sys.exit(1)
    DBG = namespace['DBG']
    client = mqtt.Client(client_id=namespace['MQTT_CLIENT_ID'])
    client.topics = namespace['TOPICS']
    client.username_pw_set(namespace['MQTT_USERNAME'], namespace['MQTT_PASSWORD'])
    client.on_connect = on_connect
    client.on_message = on_message
    
    repub = repubmqtt.Republish(namespace['RULES'], client, namespace['xlate'], namespace['DBG'])
    client.repub = repub
    
    client.connect(namespace['MQTT_SERVER'], namespace['MQTT_PORT'], 60)
    client.loop_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
