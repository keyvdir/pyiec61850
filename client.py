#!/usr/bin/python
import sys
import time
import threading
import traceback
import signal
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
    print("Starting Client At Time %s" % current_time);
    
	#Create Client Connection
    con = iec61850.IedConnection_create()
    error = iec61850.IedConnection_connect(con, "localhost", 8102);
    
    if (error == iec61850.IED_ERROR_OK):
        [deviceList, error] = iec61850.IedConnection_getLogicalDeviceList(con)
        device = iec61850.LinkedList_getNext(deviceList)
        
        print("Connected to Server.\n")
        
		#Show Logical Node, Logical Device and Data Object inside the Server
        while device:
            LD_name=iec61850.toCharP(device.data)
            print("LD: %s" % LD_name)
            [logicalNodes, error] = iec61850.IedConnection_getLogicalDeviceDirectory(con, LD_name)
            logicalNode = iec61850.LinkedList_getNext(logicalNodes)
            while logicalNode:
                LN_name=iec61850.toCharP(logicalNode.data)
                print(" LN: %s" % LN_name)
                [LNobjects, error] = iec61850.IedConnection_getLogicalNodeVariables(con, LD_name+"/"+LN_name)
                LNobject = iec61850.LinkedList_getNext(LNobjects)
                while LNobject:
                    print("  DO: %s" % iec61850.toCharP(LNobject.data))
                    LNobject = iec61850.LinkedList_getNext(LNobject)
                iec61850.LinkedList_destroy(LNobjects)
                logicalNode = iec61850.LinkedList_getNext(logicalNode)
            iec61850.LinkedList_destroy(logicalNodes)
            device = iec61850.LinkedList_getNext(device)
        iec61850.LinkedList_destroy(deviceList)
        
        running = 1;
    
        signal.signal(signal.SIGINT, signal_handler);
        
        while (running):
            #Read Data Object
            theVal = "testmodelSENSORS/TTMP1.Temp1.float"
            theValType = iec61850.IEC61850_FC_MX
            value = iec61850.IedConnection_readFloatValue(con, theVal, theValType);
            print("\n Read Value of TTMP1.Temp1.float: %s" % value[0]);
            
            assert(value[1]==0)
            newValue= value[0]
            err = iec61850.IedConnection_writeFloatValue(con, theVal, theValType, newValue)
            assert(err==25)
        
            # Accessing to ASG values
            theVal = "testmodelSENSORS/TTMP1.TmpSp.setMag.f"
            theValType = iec61850.IEC61850_FC_SP
            setpoint = iec61850.IedConnection_readFloatValue(con, theVal, theValType)
            assert(value[1]==0)
            newValue= 50
            err = iec61850.IedConnection_writeFloatValue(con, theVal, theValType, newValue)
            assert(err==0)
			#Write Data Object with new value
            setpoint = iec61850.IedConnection_readFloatValue(con, theVal, theValType)
            print(" Write Value of TTMP1.Temp1.float: %s" % setpoint[0])
            assert(setpoint[0]==newValue)
        
            #Read Data Object
            theVal1 = "testmodelSENSORS/TTMP1.Temp1.string"
            theValType1 = iec61850.IEC61850_FC_DC
            value1 = iec61850.IedConnection_readStringValue(con, theVal1, theValType1);
            print(" Read Value of TTMP1.Temp1.string: %s" % value1[0]);
            
            assert(value1[1]==0)
            newValue1= value1[0]
            err1 = iec61850.IedConnection_writeVisibleStringValue(con, theVal1, theValType1, newValue1)
            assert(err1==21)
        
            # Accessing to VSG values
            theVal1 = "testmodelSENSORS/TTMP1.TmpSt.setVal"
            theValType1 = iec61850.IEC61850_FC_SP
            setpoint1 = iec61850.IedConnection_readStringValue(con, theVal1, theValType1)
            assert(value1[1]==0)
            newValue1= "Networked System Lab"
            err1 = iec61850.IedConnection_writeVisibleStringValue(con, theVal1, theValType1, newValue1)
            assert(err1==0)
			#Write Data Object with new value
            setpoint1 = iec61850.IedConnection_readStringValue(con, theVal1, theValType1)
            print(" Write Value of TTMP1.Temp1.string: %s" % setpoint1[0])
            assert(setpoint1[0]==newValue1)
            
            time.sleep(5)
        
    else:
        print("Connection error")
        sys.exit(-1)
    
    iec61850.IedConnection_close(con)
    iec61850.IedConnection_destroy(con)
    print("\n Client Disconnected.")