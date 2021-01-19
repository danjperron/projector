#!/usr/bin/python3
import serial
import time

'''
Copyright <2020> <Daniel Perron>

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software
and associated documentation files (the "Software"),
to deal in the Software without restriction,
including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software,and to permit persons
to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall
be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE
'''

'''
  This class is to interface with the 8mm projector
  using stepper motor driver directly connected to the
  drive transmission of the projector. The purpose is to detect
  the fork movement to snapshot each frames of the 8mm movie film.
  simple commands are available using the serial USB port at 9600 baud.
  '0' -> Turn light OFF.
  '1' -> Turn light ON.
  'C' -> Clear Frame Counter.
  'N' -> Move motor to next frame.
  'S' -> Stop motor.
  'I' -> Get status info.
  Each command will respond with status in numeric ascii form.
  All values are separated by a tab.
  values in order,
    lightFlag -> 0=Light OFF  1=Light ON
    motorFlag -> 0=Motor is not moving  1= motor is moving
    frameCount -> frame count
    cposition  -> current Stepper position
'''


class Arduino:

    def __init__(self, port="/dev/ttyACM0"):
        try:
            self.com = serial.Serial(port=port, baudrate=9600, timeout=1)
        except serial.serialutil.SerialException:
            self.com = None

        self.flush()
        time.sleep(0.1)
        self.lightValue = False
        self.frameCount = 0
        Flag, lightFlag, motorFlag, \
            frameCount, stepperPosition = self.getStatus()
        if Flag:
            self.frameCount = frameCount
            self.lightValue = lightFlag

    def toggleLight(self):
        self.light(not self.lightValue)
        self.clrStatus()

    def light(self, value):
        if self.com is None:
            return
        self.lightValue = value
        code = b"0"
        if value:
            code = b"1"
        self.com.write(code)
        time.sleep(0.1)
        self.clrStatus()

    def close(self):
        if self.com is None:
            return
        self.flush()
        self.com.close()

    def readStatus(self):
        Flag = False
        lightFlag = False
        motorFlag = False
        frameCount = 0
        stepperPosition = 0
        if self.com is not None:
            rawline = self.com.readline()
            line = rawline.decode("utf-8").split("\r")[0]
            if len(line) > 0:
                data = line.split("\t")
                if len(data) == 4:
                    Flag = True
                    lightFlag = bool(int(data[0]))
                    motorFlag = bool(int(data[1]))
                    frameCount = int(data[2])
                    stepperPosition = int(data[3])
        return Flag, lightFlag, motorFlag, frameCount, stepperPosition

    def write(self, data):
        if self.com is not None:
            self.com.write(data)

    def flush(self):
        if self.com is not None:
            self.com.flush()

    def getStatus(self):
        self.write(b"I")
        return self.readStatus()

    def clrStatus(self):
        Flag, lightFlag, motorFlag, \
            frameCount, stepperPosition = self.readStatus()
        if self.com is not None:
            self.flush()

    def clrFrame(self):
        self.write(b"C")
        self.frameCount = 0
        self.clrStatus()

    def stop(self):
        self.write(b"S")
        self.clrStatus()

    def next(self):
        startTime = time.time()
        self.write(b"N")
        # ok wait until 5 second before exit with error
        while (time.time()-startTime) < 3.0:
            Flag, lightFlag, motorFlag, \
                frameCount, stepperPosition = self.readStatus()
            if Flag:
                if motorFlag == 0:
                    self.frameCount = frameCount
                    return True
            self.flush()
            time.sleep(0.2)
            self.write(b"I")
        time.sleep(0.2)
        self.flush()
        return False
