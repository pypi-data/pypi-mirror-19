import paho.mqtt.client as mqtt
import repubmqtt
import json
import sys
import time
import requests

DBG = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	repubmqtt.dbgprint(1, "Connected with result code "+str(rc))

	for topic in client.topics:
		client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	repubmqtt.dbgprint(1, "%s  %s" % (msg.topic, msg.payload))

	try:
		jrecord = json.loads(msg.payload.decode('utf-8')
)
	except Exception as e:
		jrecord = {'rawvalue': msg.payload }
		repubmqtt.dbgprint(1, "payload not json '%s':  %s" %(e, msg.topic+" "+str(msg.payload)))
	jrecord['topic'] = msg.topic
	userdata.process_message(jrecord)


def publish_mqtt(publish, output_data, data):
	topic = publish['topic'] % data
	retain = publish.get('retain',False)
	if publish['_testmode']:
		repubmqtt.log('test', "publish_mqtt %s %s" % (topic, output_data))
		return
	client.publish(topic, output_data, retain=retain)


restful_cache = {}
def publish_restful(publish,  output_data, data):
	url = publish['url'] % data
	headers = publish['headers']
	if publish['_testmode']:
		repubmqtt.log('test', "publish_restful (%s) %s" % (url, output_data))
		return

	now = time.time()
	if not url in restful_cache or (restful_cache[url]['ts'] + 60) < now:
		rsession = {}
		restful_cache[url] = rsession
		rsession['sess'] = requests.Session()
		rsession['ts'] = now
	else:
		rsession = restful_cache[url]
	sess = rsession['sess']
	response = sess.post(url, data=output_data, headers=headers)

#
# 
REQUIRED_NAMES = ['MQTT_SERVER', 'MQTT_PORT', 'MQTT_CLIENT_ID', 'MQTT_USERNAME', 'MQTT_PASSWORD',
	 'TOPICS', 'RULES', 'xlate']

def main():
	global DBG, client
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
	repub = repubmqtt.Republish(namespace['RULES'], namespace['xlate'])
	repub.setdebuglevel(namespace['DBG'])
	repub.register_publish_protocol('mqtt', publish_mqtt)
	repub.register_publish_protocol('restful', publish_restful)

	client = mqtt.Client(client_id=namespace['MQTT_CLIENT_ID'], userdata=repub)
	client.topics = namespace['TOPICS']
	client.username_pw_set(namespace['MQTT_USERNAME'], namespace['MQTT_PASSWORD'])
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(namespace['MQTT_SERVER'], namespace['MQTT_PORT'], 60)
	client.loop_forever()
	return 0


if __name__ == "__main__":
	sys.exit(main())
