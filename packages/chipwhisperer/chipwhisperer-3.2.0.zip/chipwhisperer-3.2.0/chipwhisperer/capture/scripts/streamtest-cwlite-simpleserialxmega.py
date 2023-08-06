#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014, NewAE Technology Inc
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
#=================================================

from chipwhisperer.common.api.CWCoreAPI import CWCoreAPI  # Import the ChipWhisperer API
from chipwhisperer.common.scripts.base import UserScriptBase

import time

class UserScript(UserScriptBase):
    _name = "Debug"
    _description = "Debug"

    def __init__(self, api):
        super(UserScript, self).__init__(api)

    def streamTest(self):

        self.scope = self.api.getScope()
        self.target = self.api.getTarget()


        nae = self.scope.scopetype.ser
        dbuf = [0] * nae.cmdReadStream_bufferSize(200000)

        self.scope.arm()
        #self.target.go()

        _, rx_bytes = nae.cmdReadStream(200000, dbuf, timeout_ms=5000)

        # Disarm scope
        self.scope.qtadc.sc.arm(False)

        # Process data
        bsize = nae.cmdReadStream_size_of_fpgablock()

        dbuf2 = [0] * nae.cmdReadStream_bufferSize(200000)
        dbuf2[0] = dbuf[0]
        dbuf2_idx = 1
        for i in range(0, rx_bytes, bsize):
            if dbuf[i] != 0xAC:
                print "shit"
                break
            s = i + 1
            dbuf2[dbuf2_idx : (bsize-1)] = dbuf[s:(s+(bsize-1))]

            #Write to next section
            dbuf2_idx += (bsize-1)

        processed_data = self.scope.qtadc.sc.processData(dbuf2, 0.0)

        print len(processed_data)


    def run(self):
        # User commands here
        self.api.setParameter(['Generic Settings', 'Scope Module', 'ChipWhisperer/OpenADC'])
        #self.api.setParameter(['Generic Settings', 'Target Module', 'Simple Serial'])
        self.api.setParameter(['Generic Settings', 'Trace Format', 'ChipWhisperer/Native'])
        self.api.setParameter(['Simple Serial', 'Connection', 'NewAE USB (CWLite/CW1200)'])
        self.api.setParameter(['ChipWhisperer/OpenADC', 'Connection', 'NewAE USB (CWLite/CW1200)'])
                
        self.api.connect()
        
        # Example of using a list to set parameters. Slightly easier to copy/paste in this format
        lstexample = [['CW Extra Settings', 'Trigger Pins', 'Target IO4 (Trigger Line)', True],
                      ['CW Extra Settings', 'Target IOn Pins', 'Target IO1', 'Serial RXD'],
                      ['CW Extra Settings', 'Target IOn Pins', 'Target IO2', 'Serial TXD'],
                      ['OpenADC', 'Clock Setup', 'CLKGEN Settings', 'Desired Frequency', 5000000],
                      ['CW Extra Settings', 'Target HS IO-Out', 'CLKGEN'],
                      ['OpenADC', 'Clock Setup', 'ADC Clock', 'Source', 'CLKGEN x1 via DCM'],
                      ['OpenADC', 'Trigger Setup', 'Total Samples', 3000],
                      ['OpenADC', 'Trigger Setup', 'Offset', 1250],
                      ['OpenADC', 'Gain Setting', 'Setting', 45],
                      ['OpenADC', 'Trigger Setup', 'Mode', 'low'],
                      # Final step: make DCMs relock in case they are lost
                      ['OpenADC', 'Clock Setup', 'ADC Clock', 'Reset ADC DCM', None],
                      ]
        
        # Download all hardware setup parameters
        for cmd in lstexample: self.api.setParameter(cmd)
        
        # Let's only do a few traces
        self.api.setParameter(['Generic Settings', 'Acquisition Settings', 'Number of Traces', 50])
                      
        # Throw away first few
        self.api.capture1()
        self.api.capture1()

        #Switch to streaming mode
        #oa = self.api.getScope().qtadc.sc
        #base = oa.sendMessage(0x80, 1)[0]
        #oa.sendMessage(0xC0, 1, [base | (1<<4)])
        #self.oa = oa

        #self.streamTest()


        # Capture a set of traces and save the project
        # self.api.captureM()
        # self.api.saveProject("../../../projects/test.cwp")


if __name__ == '__main__':
    import chipwhisperer.capture.ui.CWCaptureGUI as cwc         # Import the ChipWhispererCapture GUI
    from chipwhisperer.common.utils.parameter import Parameter  # Comment this line if you don't want to use the GUI
    Parameter.usePyQtGraph = True                               # Comment this line if you don't want to use the GUI
    api = CWCoreAPI()                                           # Instantiate the API
    app = cwc.makeApplication("Capture")                        # Change the name if you want a different settings scope
    gui = cwc.CWCaptureGUI(api)                                 # Comment this line if you don't want to use the GUI
    gui.show()                                                  # Comment this line if you don't want to use the GUI
    api.runScriptClass(UserScript)                              # Run the User Script (executes "run()" by default)
    app.exec_()                                                 # Comment this line if you don't want to use the GUI
