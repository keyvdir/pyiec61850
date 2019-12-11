#!/usr/bin/python
import sys
import time
import threading
import traceback
import signal
import Adafruit_DHT
import sys
sys.path.insert(0, "~/libiec61850/pyiec61850")
import iec61850
from datetime import datetime

def signal_handler(signal, frame):
    global running
    running =0
    print('You pressed Ctrl+C!')

    
if __name__=="__main__":
    now = datetime.now();
    current_time = now.strftime("%H:%M:%S");
    print("Starting MMS Server At Time %s" % current_time);
    
	#Create Model IED
    myModel = iec61850.IedModel_create("testmodel");
	#Create Logical Device
    lDevice1 = iec61850.LogicalDevice_create("SENSORS", myModel);
	#Create Logical Node
    ttmp1 = iec61850.LogicalNode_create("TTMP1", lDevice1);
	#Create Model Node
    iec61850.CDC_ASG_create("TmpSp",  iec61850.toModelNode(ttmp1), 0, False);
    iec61850.CDC_VSG_create("TmpSt",  iec61850.toModelNode(ttmp1), 0);
	#Create Data Object
    do1 = iec61850.DataObject_create("Temp1", iec61850.toModelNode(ttmp1), 0);
	#Create Data Attribute
    fl = iec61850.DataAttribute_create("float", iec61850.toModelNode(do1), iec61850.IEC61850_FLOAT64, iec61850.IEC61850_FC_MX, 0, 0, 0);
    st = iec61850.DataAttribute_create("string", iec61850.toModelNode(do1), iec61850.IEC61850_VISIBLE_STRING_255, iec61850.IEC61850_FC_DC, 0, 0, 0);
    
    #Create Server Connection
    iedServer = iec61850.IedServer_create(myModel);
    iec61850.IedServer_start(iedServer, 8102);
    print("Waiting for connection...\n");
    
    
    if not(iec61850.IedServer_isRunning(iedServer)) :
        print("Starting server failed! Exit.\n");
        iec61850.IedServer_destroy(iedServer);
        sys.exit(-1);
    
    running = 1;
    
    signal.signal(signal.SIGINT, signal_handler);
    
    #Main loop
    while (running):
		#Sensing humidity and temperature value using DHT11
        humidity, temperature = Adafruit_DHT.read_retry(11, 4);
		#Add the value to the specific Data Attribute
        val1 = iec61850.IedServer_updateFloatAttributeValue(iedServer, fl, temperature);
        val2 = iec61850.IedServer_updateVisibleStringAttributeValue(iedServer, st, 'This is');
        time.sleep(1);
    
    iec61850.IedServer_stop(iedServer);
    iec61850.IedServer_destroy(iedServer);