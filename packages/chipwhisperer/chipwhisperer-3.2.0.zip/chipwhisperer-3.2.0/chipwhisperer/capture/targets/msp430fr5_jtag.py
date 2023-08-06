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

from subprocess import call

import pickle

#Must do pip install pyserial
from PyCRC.CRCCCITT import CRCCCITT


class MSP430FR5TargetJTAG(TargetTemplate):
    _name = 'MSP430FR5xxx JTAG'

    def __init__(self):
        TargetTemplate.__init__(self)
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
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Clock Setup', 'CLKGEN Settings', 'Desired Frequency', 64000000.0])
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Trigger Setup', 'Mode', 'falling edge'])
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Clock Setup', 'Reset DCMs', None])
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Trigger Setup', 'Timeout (secs)', 10.0],)
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Gain Setting', 'Mode', 'high'])
        CWCoreAPI.getInstance().setParameter(['OpenADC', 'Gain Setting', 'Setting', 35],)

        self.oa = scope.qtadc.ser

        self.connectStatus.setValue(True)


    def close(self):
        return

    def init(self):
        return

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
        call([r"C:\ti\MSPFlasher_1.3.10\MSP430Flasher.exe", "-p", "0x%02X%02X"%(self.input[0], self.input[1])])