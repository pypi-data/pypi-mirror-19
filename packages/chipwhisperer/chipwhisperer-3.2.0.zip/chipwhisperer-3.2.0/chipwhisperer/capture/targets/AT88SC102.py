import time
import random

from chipwhisperer.common.api.CWCoreAPI import CWCoreAPI
from chipwhisperer.capture.targets._base import TargetTemplate

class AT88SC102Target(TargetTemplate):

    _name = "AT88SC102"

    def __init__(self, parentParam=None):
        super(AT88SC102Target, self).__init__(parentParam)
        self.altpin = False

        ssParams = [{'name': 'Generate Random Pin', 'key': 'randpin', 'type': 'bool', 'value': True},
                    {'name': 'Use Random Incorrect Pin', 'key': 'incorrectpin', 'type': 'bool', 'value': False},
                    {'name': 'Card Pin (Hex)', 'key': 'cardpin', 'type': 'str', 'value': 'F0F0'},
                    {'name': 'Guess Pin (Hex)', 'key': 'guesspin', 'type': 'str', 'value': 'F0F0'}
                    ]

        self.getParams().addChildren(ssParams)

    def setOpenADC(self, oadc):
        try:
            self.ser.setOpenADC(oadc)
        except:
            pass

    def getSCStatus(self):
        return self.usb.readCtrl(0x1E, dlen=1)[0]

    def reinit(self):
        self.init()

    def con(self, scope=None):
        self.usb = scope.qtadc.ser
        self.api = CWCoreAPI.getInstance()

    def init(self):
        self.usb.sendCtrl(0x1E, 0x03, [0x02])
        if self.getSCStatus() == 0:
            raise IOError("Command failed, response: %d" % self.getSCStatus())

        # Unlock card if not yet done
        self.usb.sendCtrl(0x1E, 0x03, [0x03, 0xF0, 0xF0])

        if self.getSCStatus() != 10:
            raise IOError("Command failed, response: %d" % self.getSCStatus())

        # Program random pin
        self.pin = self.get_card_pin()

        self.usb.sendCtrl(0x1E, 0x03, [0x04, self.pin[0], self.pin[1]])

        self.api.setParameter(['CW Extra Settings', 'Target Power State', False])

        # Power Cycle
        self.api.setParameter(['CW Extra Settings', 'Target Power State', False])
        time.sleep(0.25)
        self.api.setParameter(['CW Extra Settings', 'Target Power State', True])

    def setModeEncrypt(self):
        return

    def setModeDecrypt(self):
        return

    def loadEncryptionKey(self, key):
        pass

    def loadInput(self, inputtext):
        self.input = inputtext

    def isDone(self):
        return True

    def readOutput(self):
        data = [0] * 16
        data[0] = self.cardpin[0]
        data[1] = self.cardpin[1]
        data[2] = self.guesspin[0]
        data[3] = self.guesspin[1]
        return data

    def get_card_pin(self):
        if self.findParam('randpin').getValue():
            pin = [random.randint(0x00, 0xFF), random.randint(0x00, 0xFF)]
        else:
            pinint = int(self.findParam('cardpin').getValue(), 16)
            pin = [(pinint >> 8), pinint & 0xff]

        # Hack for bit-wise T-Test stuff
        # if self.altpin:
        #    self.altpin = False
        #    pin = [random.randint(0x00, 0xFF), random.randint(0x00, 0xFF)]
        #    pin[0] |= 1 << 1
        # else:
        #    pin = [random.randint(0x00, 0xFF), random.randint(0x00, 0xFF)]
        #    pin[0] &= ~(1 << 1)
        #    self.altpin = True

        self.findParam('cardpin').setValue("%02x%02x" % (pin[0], pin[1]))
        self.cardpin = pin
        return pin

    def get_guess_pin(self):
        if self.findParam('incorrectpin').getValue():
            pin = [random.randint(0x00, 0xFF), random.randint(0x00, 0xFF)]
        else:
            if self.findParam('randpin').getValue():
                pin = self.pin
            else:
                pinint = int(self.findParam('guesspin').getValue(), 16)
                pin = [(pinint >> 8), pinint & 0xff]

        self.findParam('randpin').setValue("%02x%02x" % (pin[0], pin[1]))
        self.guesspin = pin
        return pin

    def go(self):
        self.usb.sendCtrl(0x1E, 0x03, [0x02])
        if self.getSCStatus() == 0:
            raise IOError("Command failed, response: %d" % self.getSCStatus())

        pin = self.get_guess_pin()

        # Try guess pin
        print "Sending pin %s " % str(pin),
        self.usb.sendCtrl(0x1E, 0x03, [0x03, pin[0], pin[1]])
        # sendCtrl(0x1E, 0x03, [0x06, 1, pin[0], pin[1]])

        if self.getSCStatus() == 10:
            print " [OK]"
        else:
            print " [FAIL]"

        # If using incorrect pin, fix now by unlocking with correct pin
        self.usb.endCtrl(0x1E, 0x03, [0x03, self.pin[0], self.pin[1]])
        self.usb.sendCtrl(0x1E, 0x03, [0x04, 0xF0, 0xF0])

    def checkEncryptionKey(self, kin):
        return kin
