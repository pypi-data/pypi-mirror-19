#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014, NewAE Technology Inc
# All rights reserved.
#
# Author: Colin O'Flynn
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

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    print "ERROR: PySide is required for this program"
    sys.exit()

from chipwhisperer.analyzer.preprocessing._base import PreprocessingBase
from openadc.ExtendedParameter import ExtendedParameter
from pyqtgraph.parametertree import Parameter

# from functools import partial
# import scipy as sp
import numpy as np
        
class AOFFilter(PreprocessingBase):
    """
    Does Stuff
    """
     
    def setupParameters(self):
        ssParams = [{'name':'Enabled', 'type':'bool', 'value':True, 'set':self.setEnabled},
                         {'name':'Desc', 'type':'text', 'value':self.descrString}
                      ]
        self.params = Parameter.create(name='Filter', type='group', children=ssParams)
        ExtendedParameter.setupExtended(self.params, self)

    def init(self):
        project = self.parent.proj
        section = project.getDataConfig("Template Data", "AOF Matrix")
        fname = project.convertDataFilepathAbs(section[0]["filename"])
        self.H = np.load(fname)

   
    def getTrace(self, n):
        if self.enabled:
            trace = self.trace.getTrace(n)
            if trace is None:
                return None
            
            # self.tracelist.append(trace)
            # H = np.mean(self.tracelist, axis=0) / np.var(self.tracelist, axis=0)
            filttrace = np.convolve(trace, self.H, 'valid')
            # filttrace = trace * self.H

            return filttrace
            
        else:
            return self.trace.getTrace(n)       

