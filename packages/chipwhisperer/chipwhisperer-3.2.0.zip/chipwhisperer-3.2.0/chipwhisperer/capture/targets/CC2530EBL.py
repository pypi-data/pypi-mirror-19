#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014, NewAE Technology Inc
# All rights reserved.
#
# Find this and more at newae.com - this file is part of the chipwhisperer
# project, http://www.assembla.com/spaces/chipwhisperer
#
#    This file is part of chipwhisperer.
#
#    chipwhisperer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    chipwhisperer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with chipwhisperer.  If not, see <http://www.gnu.org/licenses/>.
#=================================================
import time
import pickle

from TargetTemplate import TargetTemplate
from chipwhisperer.common.utils.Scan import scan
from chipwhisperer.common.api.config_parameter import ConfigParameter
from chipwhisperer.hardware.naeusb.serial import USART as CWL_USART
from chipwhisperer.common.api.CWCoreAPI import CWCoreAPI

data = pickle.load(open(r'C:\Users\colin\Dropbox (NewAE Technology Inc)\engineering\research\targets\hue_lux_zll\fw16jan2016_update\oldbridge\ser1_main_payload.p', 'r'))

def getInstance(*args):
    return CC2530EBL(*args)

class CC2530EBL_ChipWhispererLite(TargetTemplate):
    def setupParameters(self):
        ssParams = [{'name':'baud', 'type':'int', 'key':'baud', 'value':115200, 'limits':(500, 2000000), 'get':self.baud, 'set':self.setBaud}]

        self.params = ConfigParameter.create_extended(self, name='Serial Port Settings', type='group', children=ssParams)
        self.cwlite_usart = None
        self.oa = None

    def setBaud(self, baud):
        if self.cwlite_usart:
            self.cwlite_usart.init(baud)
        else:
            print "Baud rate not set, need to connect first"
    
    def baud(self):
        return 115200
        
    def write(self, string):
        self.cwlite_usart.write(string)

    def inWaiting(self):
        return self.cwlite_usart.inWaiting()

    def read(self, num=0, timeout=250):
        data = bytearray(self.cwlite_usart.read(num, timeout=timeout))

        #result = "".join([chr(i) for i in data])
        result = data.decode('latin-1')
        return result

    def flush(self):
        waiting = self.inWaiting()
        while waiting > 0:
            self.cwlite_usart.read(waiting)
            waiting = self.inWaiting()

    def flushInput(self):
        self.flush()

    def close(self):
        pass

    def con(self):
        self.params.getAllParameters()
        self.cwlite_usart = CWL_USART(self.oa)
        self.cwlite_usart.init(baud=self.findParam('baud').value())
        self.connectStatus.setValue(True)

    def setOpenADC(self, oa):
        self.oa = oa
        
    def selectionChanged(self):
        pass

class CC2530EBL(TargetTemplate):
    def setupParameters(self):

        ser_cons = {}
        ser_cons["ChipWhisperer-Lite"] = CC2530EBL_ChipWhispererLite()
        
        defser = ser_cons["ChipWhisperer-Lite"]
        
        
        ssParams = [{'name':'Connection', 'type':'list', 'key':'con', 'values':ser_cons,'value':defser, 'set':self.setConnection},
                    {'name':'Index within Block to attack', 'type':'int', 'key':'bnum', 'value':0},
                    {'name':'Block to attack', 'type':'int', 'key':'blocknum', 'value':0},
                    {'name':'Sleep Time(s)', 'type':'float', 'key':'sleeptime', 'value':1.5},
                    ]
        self.params = ConfigParameter.create_extended(self, name='Target Connection', type='group', children=ssParams)
        self.oa = None
        self.setConnection(self.findParam('con').value())

    def setOpenADC(self, oadc):
        self.oa = oadc
        if hasattr(self.ser, "setOpenADC"):
            self.ser.setOpenADC(oadc)

    def setConnection(self, con):
        self.ser = con
        self.paramListUpdated.emit()
        if self.oa and hasattr(self.ser, "setOpenADC"):
            self.ser.setOpenADC(self.oa)
        self.ser.selectionChanged()

    def fake_aux_traceArm(self):

        bnum = self.findParam('bnum').value()
        block = self.findParam('blocknum').value()
        sleeptime = self.findParam('sleeptime').value()

        CWCoreAPI.getInstance().setParameter(['GPIO Toggle', 'Toggle Now', None])
        time.sleep(0.05)
        self.ser.flushInput()
        self.ser.write("\xff\xff\xfe\x00\x00\x00\x00")
        time.sleep(0.05)
        self.ser.flushInput()
        if block == 0 and bnum == 0:
            return

        #First block (not used?)
        self.ser.write(data[0][0])
        time.sleep(0.05)
        self.ser.flushInput()

        if block == 0 and bnum == 1:
            return

        #Second block (causes page erase)
        self.ser.write(data[0][1])

        #Do the rest now
        for b in range(1, block):
            for d in range(0, 32):
                time.sleep(0.05)
                self.ser.flushInput()
                self.ser.write(data[b][d])

        for d in range(0, bnum):
            time.sleep(0.05)
            self.ser.flushInput()
            self.ser.write(data[block][d])

        time.sleep(0.05)
        self.ser.flushInput()
        time.sleep(sleeptime)

    def paramList(self):
        p = [self.params]
        if self.ser is not None:
            for a in self.ser.paramList(): p.append(a)
        return p

    def con(self):
        self.ser.con()
        # 'x' flushes everything & sets system back to idle
        self.ser.flush()
        self.connectStatus.setValue(True)

        #Hacks away
        CWCoreAPI.getInstance().auxList[0].traceArm = self.fake_aux_traceArm

    def close(self):
        if self.ser != None:
            self.ser.close()
            # self.ser = None
        return

    def init(self):
        pass

    def setModeEncrypt(self):
        return

    def setModeDecrypt(self):
        return

    def loadInput(self, inputtext):
        return

    def isDone(self):
        return True

    def readOutput(self):
        self.newInputData.emit(self.ser.read(256))
        return None

    def go(self):
        bnum = self.findParam('bnum').value()
        block = self.findParam('blocknum').value()
        self.ser.flushInput()
        self.ser.write(data[block][bnum])
        time.sleep(0.05)

    def validateSettings(self):
        return []

    def getName(self):
        return "CC2530 EBL Hacking"