#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2016, NewAE Technology Inc
# All rights reserved.
#
# Authors: Colin O'Flynn, Greg d'Eon
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

# Class Crc
#############################################################
# These CRC routines are copy-pasted from pycrc, which are:
# Copyright (c) 2006-2013 Thomas Pircher <tehpeh@gmx.net>
#
class Crc(object):
    """
    A base class for CRC routines.
    """

    def __init__(self, width, poly):
        """The Crc constructor.

        The parameters are as follows:
            width
            poly
            reflect_in
            xor_in
            reflect_out
            xor_out
        """
        self.Width = width
        self.Poly = poly


        self.MSB_Mask = 0x1 << (self.Width - 1)
        self.Mask = ((self.MSB_Mask - 1) << 1) | 1

        self.XorIn = 0x0000
        self.XorOut = 0x0000

        self.DirectInit = self.XorIn
        self.NonDirectInit = self.__get_nondirect_init(self.XorIn)
        if self.Width < 8:
            self.CrcShift = 8 - self.Width
        else:
            self.CrcShift = 0

    def __get_nondirect_init(self, init):
        """
        return the non-direct init if the direct algorithm has been selected.
        """
        crc = init
        for i in range(self.Width):
            bit = crc & 0x01
            if bit:
                crc ^= self.Poly
            crc >>= 1
            if bit:
                crc |= self.MSB_Mask
        return crc & self.Mask


    def bit_by_bit(self, in_data):
        """
        Classic simple and slow CRC implementation.  This function iterates bit
        by bit over the augmented input message and returns the calculated CRC
        value at the end.
        """
        # If the input data is a string, convert to bytes.
        if isinstance(in_data, str):
            in_data = [ord(c) for c in in_data]

        register = self.NonDirectInit
        for octet in in_data:
            for i in range(8):
                topbit = register & self.MSB_Mask
                register = ((register << 1) & self.Mask) | ((octet >> (7 - i)) & 0x01)
                if topbit:
                    register ^= self.Poly

        for i in range(self.Width):
            topbit = register & self.MSB_Mask
            register = ((register << 1) & self.Mask)
            if topbit:
                register ^= self.Poly

        return register ^ self.XorOut

        
class BootloaderTarget(TargetTemplate):
    _name = 'AES Bootloader'

    def __init__(self, parentParam=None):
        TargetTemplate.__init__(self, parentParam)

        ser_cons = pluginmanager.getPluginsInDictFromPackage("chipwhisperer.capture.targets.simpleserial_readers", True, False, self)
        self.ser = ser_cons[SimpleSerial_ChipWhispererLite._name]

        self.keylength = 16
        self.input = ""
        self.crc = Crc(width=16, poly=0x1021)
        self.setConnection(self.ser)

    def setKeyLen(self, klen):
        """ Set key length in BITS """
        self.keylength = klen / 8        
 
    def keyLen(self):
        """ Return key length in BYTES """
        return self.keylength

    def getConnection(self):
        return self.ser

    def setConnection(self, con):
        self.ser = con
        self.params.append(self.ser.getParams())
        self.ser.connectStatus.connect(self.connectStatus.emit)
        self.ser.selectionChanged()

    def con(self, scope=None):
        if not scope or not hasattr(scope, "qtadc"): Warning(
            "You need a scope with OpenADC connected to use this Target")

        self.ser.con(scope)
        # 'x' flushes everything & sets system back to idle
        self.ser.write("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.ser.flush()
        self.connectStatus.setValue(True)

    def close(self):
        if self.ser != None:
            self.ser.close()
        return

    def init(self):
        pass

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
        self.input = inputtext

    def readOutput(self):
        # No actual output
        return [0] * 16

    def isDone(self):
        return True

    def checkEncryptionKey(self, kin):
        return kin

    def go(self):
        # Starting byte is 0x00
        message = [0x00]

        # Append 16 bytes of data
        message.extend(self.input)

        # Append 2 bytes of CRC for input only (not including 0x00)
        crcdata = self.crc.bit_by_bit(self.input)

        message.append(crcdata >> 8)
        message.append(crcdata & 0xff)

        # Write message
        message = self.convertVarToString(message)
        for i in range(0, 5):
            self.ser.flush()
            self.ser.write(message)
            time.sleep(0.1)
            data = self.ser.read(1)

            if len(data) > 0:
                resp = ord(data[0])

                if resp == 0xA4:
                    # Encryption run OK
                    break

                if resp != 0xA1:
                    raise IOError("Bad Response %x" % resp)

        if len(data) > 0:
            if resp != 0xA4:
                raise IOError("Failed to communicate, last response: %x" % resp)
        else:
            raise IOError("Failed to communicate, no response")
