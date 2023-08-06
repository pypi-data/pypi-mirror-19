#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2016, NewAE Technology Inc
# All rights reserved.
#
# Authors: Colin O'Flynn
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
# =================================================

import sys
import time
import chipwhisperer.capture.ui.CWCaptureGUI as cwc
from chipwhisperer.common.api.CWCoreAPI import CWCoreAPI
from chipwhisperer.capture.targets.SimpleSerial import SimpleSerial
from chipwhisperer.common.scripts.base import UserScriptBase
from chipwhisperer.capture.targets._base import TargetTemplate
from chipwhisperer.common.utils import pluginmanager
from chipwhisperer.capture.targets.simpleserial_readers.cwlite import SimpleSerial_ChipWhispererLite
from chipwhisperer.common.utils.parameter import setupSetParam
from chipwhisperer.hardware.naeusb.serial import USART as CWL_USART
import logging

import pickle


class SAMR21EBLTarget(TargetTemplate):
    _name = 'SAMR21EBL Bootloader'

    def __init__(self):
        TargetTemplate.__init__(self)

        self.params.addChildren([
            {'name':'bvalue', 'key':'bvalue', 'type':'int', 'range':(0, 256), 'value':0},
            {'name':'pvalue', 'key':'pvalue', 'type':'int', 'range':(0, 300), 'value':0},
            ])

        self.keylength = 16
        self.input = ""

    def setKeyLen(self, klen):
        """ Set key length in BITS """
        self.keylength = klen / 8

    def keyLen(self):
        """ Return key length in BYTES """
        return self.keylength


    def _con(self, scope=None):
        if not scope or not hasattr(scope, "qtadc"): Warning(
            "You need a scope with OpenADC connected to use this Target")

        #Setup the reset pin
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn Pins', 'Target IO3', 'GPIO'])
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'Target IO3: GPIO', 'High'])

        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn Pins', 'Target IO1', 'Serial RXD'])
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn Pins', 'Target IO2', 'Serial TXD'])
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Trigger Pins', 'Target IO2 (Serial RXD)', True])
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Trigger Pins', 'Target IO4 (Trigger Line)', False])
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Trigger Module', 'Digital IO Decode'])
        CWCoreAPI.getInstance().setParameter(['ChipWhisperer/OpenADC', 'I/O Decoder Trigger Module', 'Baud', 115200])

        self.oa = scope.qtadc.ser

        self.cwlite_usart = CWL_USART(self.oa)
        self.cwlite_usart.init(baud=115200)
        self.flush()
        self.connectStatus.setValue(True)

        #List of valid packets
        logging.info("Loading data-file")
        self.datalist = pickle.load(
            open(r"C:\Users\colin\dropbox\engineering\research\targets\hue_lux_zll\fw9july2016_update\txframes.p",
                 "rb"))

    def write(self, string):
        self.cwlite_usart.write(string)

    def read(self, num=0, timeout=250):
        data = bytearray(self.cwlite_usart.read(num, timeout=timeout))

        # result = "".join([chr(i) for i in data])
        result = data.decode('latin-1')
        return result

    def inWaiting(self):
        return self.cwlite_usart.inWaiting()

    def flush(self):
        waiting = self.inWaiting()
        while waiting > 0:
            self.cwlite_usart.read(waiting)
            waiting = self.inWaiting()

    def flushInput(self):
        self.flush()

    def close(self):
        return

    def init(self):
        self.framen = 0

        self.resetChip()

    def setModeEncrypt(self):
        return

    def setModeDecrypt(self):
        return

    def convertVarToString(self, var):
        if isinstance(var, str):
            return var

        sep = ""
        s = sep.join(["%c" % b for b in var])
        return s

    def loadEncryptionKey(self, key):
        pass

    def loadInput(self, inputtext):
        #self.input = inputtext
        pnum = 0

        #pindex = self.findParam('pvalue').getValue()

        #data = self.datalist[(pindex*2)+3][4:-1]

        #if self.findParam('bvalue').getValue() != 123:
        #    data[0:16] = [self.findParam('bvalue').getValue()]*16
        #packet.extend([self.findParam('bvalue').getValue()]*16)
        #packet.extend([0x00]*48)

        #packet = [0x00, 0x01, pnum & 0xff, (pnum >> 8) & 0xff]
        #packet.extend(data)
        #packet.append(self.calc_fcs(packet))

        packet = self.datalist[(self.framen*2)+3]
        print "Loading frame %d"%self.framen

        # Set the trigger information
        trig = packet[-3:]

        CWCoreAPI.getInstance().setParameter(['ChipWhisperer/OpenADC', 'I/O Decoder Trigger Module', 'Trigger Data', str(trig)])
        self.input = packet[0:16]

    def readOutput(self):

        data = self.read(6)
        data = [ord(c) for c in data]
        if data != [0xFE, 0x01, 0x00, 0x81, 0x00, 0x80]:
            logging.error("Invalid response: %s" % str(["%02x" % t for t in data]))

        # No actual output
        return [0] * 16

    def isDone(self):
        return True

    def checkEncryptionKey(self, kin):
        return kin

    def calc_fcs(self, payload):

        fcs = 0
        for p in payload:
            fcs = fcs ^ p
        #Length
        fcs = fcs ^ 0x42
        return fcs

    def resetChip(self):
        # Reset chip
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'Target IO3: GPIO', 'Low'])
        time.sleep(0.01)
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'Target IO3: GPIO', 'High'])

        # wait for boot?
        time.sleep(0.05)

        self.flush()

        # Send start
        self.write([0xfe, 0x00])
        time.sleep(0.001)
        self.write([0x00, 0x00, 0x00])

        data = self.read(10)
        data = [ord(c) for c in data]
        if data != [0xfe, 0x05, 0x00, 0x80, 0x00, 0x01, 0x0A, 0x00, 0x6B, 0xE5]:
            logging.error("Invalid sync packet: %s" % str(["%02x" % t for t in data]))
            return

        time.sleep(0.003)

    def go(self):

        #self.resetChip()

        #Packet #1
        self.write([0xfe, 0x42])
        self.write(self.datalist[(self.framen * 2) + 3])

        self.framen = self.framen + 1


