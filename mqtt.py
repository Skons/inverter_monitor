import argparse,os
import paho.mqtt.client as mqtt
import logging, logging.handlers
import time

mqtt_host = "" #Hostname or ip of MQTT
mqtt_port = "1883" #The port where MQTT is listening
mqtt_username = "" #Username to authenticate against MQTT
mqtt_password = "" #Password for MQTT authentication
mqtt_clientname = "inverter_monitor" #The client name used for MQTT
mqtt_base_topic = "invertermonitor" #The base topic where to publish to
mqtt_include_serial = True #if true, the topic will be {mqtt_base_topic}/{serial number}
log_level = "info" #Use debug to get more details in the log

class NoneableType(object):
    def __init__(self, arg_type):
        self._type = arg_type

    def __call__(self, value):
        if value is not None:
            return self._type(value)
        return value

#Configure logging
if log_level == 'debug':
	loglevel = logging.DEBUG
else:
	loglevel = logging.INFO

scriptdir = os.path.dirname(__file__)
current_day = time.strftime("%Y%m%d")
log_file = f"{scriptdir}/logs/mqtt-{current_day}.log"
log_handler = logging.handlers.RotatingFileHandler(log_file,maxBytes=20000000,backupCount=5)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s	%(message)s','%Y-%m-%d %H:%M:%S')
log_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(loglevel)

#Define all parameters
parser = argparse.ArgumentParser()
parser.add_argument('--etoday', type=NoneableType(str), default=None, dest='etoday')
parser.add_argument('--pac', type=NoneableType(str), default=None, dest='pac')
parser.add_argument('--date', type=NoneableType(str), default=None, dest='date')
parser.add_argument('--time', type=NoneableType(str), default=None, dest='time')
parser.add_argument('--vpv1', type=NoneableType(str), default=None, dest='vpv1')
parser.add_argument('--vpv2', type=NoneableType(str), default=None, dest='vpv2')
parser.add_argument('--vpv3', type=NoneableType(str), default=None, dest='vpv3')
parser.add_argument('--temp', type=NoneableType(str), default=None, dest='temp')
parser.add_argument('--serial', type=NoneableType(str), default=None, dest='serial')
parser.add_argument('--idc1', type=NoneableType(str), default=None, dest='idc1')
parser.add_argument('--idc2', type=NoneableType(str), default=None, dest='idc2')
parser.add_argument('--idc3', type=NoneableType(str), default=None, dest='idc3')
parser.add_argument('--etotalh', type=NoneableType(str), default=None, dest='etotalh')
parser.add_argument('--etotall', type=NoneableType(str), default=None, dest='etotall')
parser.add_argument('--htotalh', type=NoneableType(str), default=None, dest='htotalh')
parser.add_argument('--htotall', type=NoneableType(str), default=None, dest='htotall')
parser.add_argument('--mode', type=NoneableType(str), default=None, dest='mode')
parser.add_argument('--err_gv', type=NoneableType(str), default=None, dest='err_gv')
parser.add_argument('--err_gf', type=NoneableType(str), default=None, dest='err_gf')
parser.add_argument('--err_gz', type=NoneableType(str), default=None, dest='err_gz')
parser.add_argument('--err_temp', type=NoneableType(str), default=None, dest='err_temp')
parser.add_argument('--err_pv1', type=NoneableType(str), default=None, dest='err_pv1')
parser.add_argument('--err_gfc1', type=NoneableType(str), default=None, dest='err_gfc1')
parser.add_argument('--err_mode', type=NoneableType(str), default=None, dest='err_mode')
parser.add_argument('--iac1', type=NoneableType(str), default=None, dest='iac1')
parser.add_argument('--vac1', type=NoneableType(str), default=None, dest='vac1')
parser.add_argument('--fac1', type=NoneableType(str), default=None, dest='fac1')
parser.add_argument('--pdc1', type=NoneableType(str), default=None, dest='pdc1')
parser.add_argument('--unk10', type=NoneableType(str), default=None, dest='unk10')
parser.add_argument('--unk11', type=NoneableType(str), default=None, dest='unk11')
parser.add_argument('--unk12', type=NoneableType(str), default=None, dest='unk12')
parser.add_argument('--unk13', type=NoneableType(str), default=None, dest='unk13')
parser.add_argument('--iac2', type=NoneableType(str), default=None, dest='iac2')
parser.add_argument('--vac2', type=NoneableType(str), default=None, dest='vac2')
parser.add_argument('--fac2', type=NoneableType(str), default=None, dest='fac2')
parser.add_argument('--pdc2', type=NoneableType(str), default=None, dest='pdc2')
parser.add_argument('--unk14', type=NoneableType(str), default=None, dest='unk14')
args = parser.parse_args()

logger.debug(f"parameters: '{args}'")

#Do the MQTT
def on_connect(client, userdata, flags, rc):
	logger.info("Connected with result code {0}".format(str(rc)))

def start_mqtt_client(mqtthost, mqttport, mqttusername, mqttpassword, mqttClientName):
	global mqtt_client
	logger.info("Connecting mqtt")
	mqtt_client = mqtt.Client(mqttClientName)
	mqtt_client.username_pw_set(username=mqttusername, password=mqttpassword)
	mqtt_client.on_connect = on_connect
	#mqtt_client.on_message = on_message
	mqtt_client.connect(host=mqtthost, port=int(mqttport))
	mqtt_client.loop_start()

start_mqtt_client(mqtt_host,mqtt_port,mqtt_username,mqtt_password,mqtt_clientname)

#Publish all parameters and values dynamically
for key,value in vars(args).items():
    if mqtt_include_serial:
        mqtt_value_topic = f"{mqtt_base_topic}/{args.serial}/{key}"
    else:
        mqtt_value_topic = f"{mqtt_base_topic}/{key}"
    result = mqtt_client.publish(mqtt_value_topic,value)
    logger.debug(f"publish: '{value}' on topic '{mqtt_value_topic}' '{bool(result.rc == mqtt.MQTT_ERR_SUCCESS)}'")