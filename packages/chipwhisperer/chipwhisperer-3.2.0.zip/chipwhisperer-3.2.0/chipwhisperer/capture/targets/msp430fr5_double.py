#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, NewAE Technology Inc
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

#This is a basic implementation of the BSL on the MSP430FR5xxx device. This will eventually be designed to
#be a stand-alone programmer, but that is not (yet) implemented and a work in progress.

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

from subprocess import call

#Must do pip install pyserial
from PyCRC.CRCCCITT import CRCCCITT


class MSP430FR5TargetBSLJTAG(TargetTemplate):
    _name = 'MSP430FR5xxx Double-JTAG-BSL'

    def __init__(self):
        TargetTemplate.__init__(self)

        #self.mode = "pwguess"
        #self.mode = "bootcap"
        #self.mode = "rebootonly"
        self.mode = "jtagpw"

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
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'nRST: GPIO', 'High'])
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'PDIC: GPIO', 'Low'])

        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn Pins', 'Target IO1', 'Serial RXD'])
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn Pins', 'Target IO2', 'Serial TXD'])
        #CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Trigger Pins', 'Target IO2 (Serial RXD)', True])
        #CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Trigger Module', 'Digital IO Decode'])
        #CWCoreAPI.getInstance().setParameter(['ChipWhisperer/OpenADC', 'I/O Decoder Trigger Module', 'Baud', 9600])

        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Clock Setup', 'CLKGEN Settings', 'Desired Frequency', 64000000.0])
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Trigger Setup', 'Mode', 'falling edge'])
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Clock Setup', 'Reset DCMs', None])
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Trigger Setup', 'Timeout (secs)', 10.0],)
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Gain Setting', 'Mode', 'high'])
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Gain Setting', 'Setting', 35],)

        self.oa = scope.qtadc.ser

        self.cwlite_usart = CWL_USART(self.oa)
        self.cwlite_usart.init(baud=9600, parity='even')
        self.flush()
        self.connectStatus.setValue(True)

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
        self.reset()

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
        if self.mode == "jtagpw":
            self.reset()
            self.reset()
            self.cmd_unlock()
            self.cmd_unlock()
            self.cmd_sendblock(blockaddr=0xff88, data=[key[1], key[0]])

            #Power cycle for new key to take effect
            CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target Power State', False])
            time.sleep(0.25)
            CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target Power State', True])
            time.sleep(0.1)



    def loadInput(self, inputtext):

        self.input = inputtext

        if self.mode == "bootcap":
            self.cmd_unlock()
            self.cmd_sendblock(blockaddr=0xFF84, data=inputtext[0:1])
            return

    def readOutput(self):
        # No actual output
        return [0] * 16

    def isDone(self):
        return True

    def checkEncryptionKey(self, kin):
        return kin

    def reset(self, enter_bootloader=True):
        # Reset chip
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'nRST: GPIO', 'Low'])
        time.sleep(0.01)

        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'PDIC: GPIO', 'Low'])

        if enter_bootloader:
            CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'PDIC: GPIO', 'High'])
            CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'PDIC: GPIO', 'Low'])
            CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'PDIC: GPIO', 'High'])
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'nRST: GPIO', 'High'])
        CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'PDIC: GPIO', 'Low'])
        time.sleep(0.01)

        self.flush()

    def go(self):
        if self.mode == "pwguess":
            passtry = list(bytearray(self.input[:]))
            passtry.extend([0xff]*16)
            print str(passtry)
            self.cmd_unlock(passtry)

        elif self.mode == "bootcap" or self.mode == "rebootonly":
            self.reset(True)

        elif self.mode == "jtagpw":
            CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'nRST: GPIO', 'Default'])
            CWCoreAPI.getInstance().setParameter(['CW Extra Settings', 'Target IOn GPIO Mode', 'PDIC: GPIO', 'Default'])
            call([r"C:\ti\MSPFlasher_1.3.10\MSP430Flasher.exe", "-p", "0x%02X%02X" % (self.input[0], self.input[1])])

        else:
            raise ValueError("Unknown mode", self.mode)

    def wrap_core(self, corecmd):

        #Build main command
        cmd_len = len(corecmd)
        cmd = [0x80, cmd_len & 0xff, (cmd_len >> 8) & 0xff]

        #Add core CMD
        cmd.extend(corecmd)

        #Calculate CRC
        crc = CRCCCITT(version='FFFF').calculate(str(bytearray(corecmd)))

        cmd.append( crc & 0xff)
        cmd.append(( crc >> 8) & 0xff)

        return cmd

    def cmd_unlock(self, passwd=[0xff]*32):

        cmd = [0x11]
        cmd.extend(passwd)
        self.write(self.wrap_core(cmd))

        resp = self.read(8)
        resp = self.cmd_parserespond(resp)

        if resp == 0x00:
            print "password OK"
        else:
            print "bad password?"

    def cmd_lock(self, passwd=[0xff]*32, ignore_length_restriction=False):
        if (len(passwd) != 32) and (ignore_length_restriction == False):
            raise ValueError("passwd must be 32 bytes long")

        self.cmd_sendblock(blockaddr = 0xFFE0, data=passwd)

    def cmd_set_eraseonfail(self, mass_erase_on_fail = True):

        #Changes sig1/sig2 to enable or disable the 'mass erase on wrong password' feature
        if mass_erase_on_fail:
            self.cmd_sendblock(blockaddr=0xFF84, data=[0xFF, 0xFF, 0xFF, 0xFF])
        else:
            self.cmd_sendblock(blockaddr = 0xFF84, data=[0xAA, 0xAA, 0xAA, 0xAA])

    def cmd_sendblock(self, blockaddr = 0, data = None):
        cmd = [0x10]
        cmd.append(blockaddr & 0xff)
        cmd.append((blockaddr >> 8) & 0xff)
        cmd.append((blockaddr >> 16) & 0xff)
        cmd.extend(data)

        self.write(self.wrap_core(cmd))
        resp = self.cmd_parserespond(self.read(32))

        if resp != 0x00:
            raise IOError("Write failure, status = %02x"%resp)

    def cmd_readblock(self, blockaddr = 0, len = 32):
        pass

    def cmd_readversion(self):
        self.write(self.wrap_core([0x19]))
        data = self.read(11)
        resp = self.cmd_parserespond(data)

        vers = {'vendor':resp[0], 'civersion':resp[1], 'apiversion':resp[2], 'piversion':resp[3]}
        logging.info("BSL ID: %02x.%02x.%02x.%02x"%(resp[0], resp[1], resp[2], resp[3]))
        return vers

    def cmd_parserespond(self, data):

        data =  bytearray(data, 'latin-1')

        if data[0] != 0x00:
            raise IOError("ACK Failed: 0x%02x != 0x00"%data[0])

        if data[1] != 0x80:
            raise IOError("Response failed, 0x%02x != 0x80"%data[1])

        datalen = data[2] | (data[3] << 8)

        if datalen > 1:

            if data[4] == 0x3A:
                return data[5:(5+(datalen-1))]
            elif data[4] == 0x3B:
                if data[5] == 0x00:
                    pass
                else:
                    logging.warning("Response status 0x3B: %02x"%data[5])
                return data[5]
            else:
                raise IOError("Unknown CMD, 0x%02x"%data[4])
