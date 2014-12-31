#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import requests
import os

class ledStripController(object):
    def __init__(self):
        """
        Object for controlling LED Strips
        """

        self.RED_PIN = 11 #Change me to the pin hooked up to red
        self.BLUE_PIN = 12 #Blue pin
        self.GREEN_PIN = 13 #Green pin

        self.DATA_URL = "http://localhost/ledController/server/displayData.php" #change if different

        self.DATA_CHECK_FREQUENCY = 1 #How often to check the data file, in Hertz

        self.ON_FREQUENCY = 50 #in Hertz;
        self.STROBE_FREQUENCY = .5 #baseline strobe frequency in Hz (if strobe slider was set to 0);

        self.OFF_DUTY_CYCLE = 0

        self.INCREMENT_STEP = 5 #increment step for fades

        GPIO.setmode(GPIO.BOARD) #change if necessary

        #Setting up pins as output pins
        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.BLUE_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)

        self.pwmRed = GPIO.PWM(self.RED_PIN, self.ON_FREQUENCY)
        self.pwmBlue = GPIO.PWM(self.BLUE_PIN, self.ON_FREQUENCY)
        self.pwmGreen = GPIO.PWM(self.GREEN_PIN, self.ON_FREQUENCY)

        self.pwmRed.start(0) #starting off at 0 duty cycle
        self.pwmGreen.start(0)
        self.pwmBlue.start(0)

        self.powerOn = True
        self.strobeOn = False
        self.strobeSpeed = 50
        self.fadeSpeed = 50
        self.brightness = 50
        self.userSetting = 0
        self.reportedRedLevel = 50 #these three reported color levels are those reported by the server and are used in userSetting 0 (solid color, no fading)
        self.reportedGreenLevel = 50
        self.reportedBlueLevel = 50
        self.redLevel = 50 #these are the levels used when fading (userSetting != 0)
        self.greenLevel = 50
        self.blueLevel = 50

        self.currentTime = time.time()

        self.strobeTime = time.time()
        self.fadeTime = time.time()
        self.lastDataCheckTime = time.time()

        self.fadeState = 0

        self.checkDataFileAndUpdate()

    def runMainLoop(self):
        """
        Call this method once to start the LED strip controlling.
        """
        while true:
            self.currentTime = time.time()

            if (self.currentTime - self.lastDataCheckTime) > (1.0/float(self.DATA_CHECK_FREQUENCY)):
                self.checkDataFileAndUpdate()

            if self.powerOn:
                if self.userSetting == 0:
                    self.setBrightness(self.pwmBlue, float(self.reportedBlueLevel))
                    self.setBrightness(self.pwmGreen, float(self.reportedGreenLevel))
                    self.setBrightness(self.pwmRed, float(self.reportedRedLevel))
                else:
                    if (self.currentTime - self.fadeTime)<(10.0/float((self.fadeSpeed + 1.0))):
                        pass
                    elif (self.currentTime - self.fadeTime)>(10.0/float((self.fadeSpeed + 1.0))):
                        self.fade(self.userSetting)
                        self.turnAllOn()
                        self.fadeTime = self.currentTime

                if strobeOn:
                    if (self.currentTime - self.strobeTime)<(.5/float(self.STROBE_FREQUENCY*(self.strobeSpeed + 1.0))):
                        turnAllOn()
                    elif (self.currentTime - self.strobeTime)>(1.0/float(self.STROBE_FREQUENCY*(self.strobeSpeed + 1.0))):
                        self.strobeTime = self.currentTime
                    else:
                        self.turnAllOff()
            else:
                self.turnAllOff()

    def turnAllOff(self):
        """
        turn off all LED's by setting duty cycle to 0
        """
        self.pwmRed.ChangeDutyCycle(OFF_DUTY_CYCLE)
        self.pwmGreen.ChangeDutyCycle(OFF_DUTY_CYCLE)
        self.pwmBlue.ChangeDutyCycle(OFF_DUTY_CYCLE)

    def setBrightness(self, pwmColor, finalBrightness):
        """
        sets brightness of an output pin by setting the pwm pin to finalBrightness*this.brightness/100 duty cycle
        """
        pwmColor.ChangeDutyCycle(finalBrightness*float(brightness)/100.0)

    def turnAllOn(self):
        """
        sets brightness of all output pins to their set levels (ie. "on")
        """
        self.setBrightness(pwmBlue,blueLevel)
        self.setBrightness(pwmGreen,greenLevel)
        self.setBrightness(pwmRed,redLevel)

    def fade(self, setting):
        """
        performs the fade as specified by the setting
        """
        if setting == 1:
            fade1()
        elif setting == 2:
            fade2()
        elif setting == 3:
            fade3()
        elif setting == 4:
            fade4()
        elif setting == 5:
            fade5()

    def incrementLevel(self, colorToIncrement):
        """
        increases colorToIncrement by INCREMENT_STEP defined in init

        colorToIncrement - string that corresponds to the color needed: "red", "green", or "blue"
        """
        self.changeLevel(colorToIncrement, self.INCREMENT_STEP)

    def decrementLevel(self, colorToDecrement):
        """
        decreases colorToDecrement by INCREMENT_STEP defined in init

        colorToDecrement - string that corresponds to the color needed: "red", "green", or "blue"
        """
        self.changeLevel(colorToDecrement, -1*self.INCREMENT_STEP)

    def changeLevel(self, colorToChange, changeStep):
        """
        increments or decrements colorToChange by changeStep

        colorToChange - string that corresponds to the color needed: "red", "green", or "blue"
        """
        if colorToChange == "red":
            self.redLevel += changeStep
        elif colorToChange == "green":
            self.greenLevel += changeStep
        elif colorToChange == "blue":
            self.blueLevel += changeStep
        else:
            print "called changeLevel with invalid color: " + colorToChange

    def checkDataFileAndUpdate(self):
        """
        checks data file and updates local variables accordingly
        """
        dataRequest = requests.get(self.DATA_URL)
        dataText = dataRequest.text

        splitData = dataText.strip().split()

        self.reportedRedLevel = splitData[1]
        self.reportedGreenLevel = splitData[2]
        self.reportedBlueLevel = splitData[3]

        self.brightness = splitData[7]
        self.fadeSpeed = splitData[9]
        self.strobeSpeed = splitData[11]

        if splitData[12] == "on":
            self.strobeOn = True
        else:
            self.strobeOn = False

        if splitData[14] == "on":
            self.powerOn = True
        else:
            self.powerOn = False

        if self.userSetting != splitData[5]:
            self.userSetting = splitData[5]
            self.fadeState = 0

    ###    Fades start here
    ###      code for defining fade behavior

    def fade1(self):
        if self.fadeState == 0:

            self.blueLevel = 100
            self.redLevel = 0
            self.greenLevel = 0

            self.fadeState = 1
        if self.fadeState == 1:
            if self.greenLevel < 100:
                self.incrementLevel("green")
            else:
                self.fadeState = 2
        if self.fadeState == 2:
            if self.redLevel < 100:
                self.incrementLevel("red")
            else:
                self.fadeState = 3
        if self.fadeState == 3:
            if self.blueLevel > 0:
                self.decrementLevel("blue")
            else:
                self.fadeState = 4
        if self.fadeState == 4:
            if self.greenLevel > 0:
                self.decrementLevel("green")
            else:
                self.fadeState = 5
        if self.fadeState == 5:
            if self.blueLevel < 100:
                self.incrementLevel("blue")
            else:
                self.fadeState = 6
        if self.fadeState == 6:
            if self.redLevel > 0:
                self.decrementLevel("red")
            else:
                self.fadeState = 1

    def fade2(self):
        if self.fadeState == 0:

            self.blueLevel = 100
            self.redLevel = 0
            self.greenLevel = 0

            self.fadeState = 1
        if self.fadeState == 1:
            if self.greenLevel < 100:
                self.incrementLevel("green")
                self.decrementLevel("blue")
            else:
                self.fadeState = 2
        if self.fadeState == 2:
            if self.redLevel < 100:
                self.incrementLevel("red")
                self.decrementLevel("green")
            else:
                self.fadeState = 3
        if self.fadeState == 3:
            if self.blueLevel < 100:
                self.incrementLevel("blue")
                self.decrementLevel("red")
            else:
                self.fadeState = 1

    def fade3(self):
        if self.fadeState == 0:

            self.blueLevel = 0
            self.redLevel = 0
            self.greenLevel = 100

            self.fadeState = 1
        if self.fadeState == 1:
            if self.greenLevel > 50:
                self.decrementLevel("green")
                self.incrementLevel("blue")
                self.incrementLevel("red")
            else:
                self.fadeState = 2
        elif self.fadeState == 2:
            if self.greenLevel > 0:
                self.decrementLevel("green")
                self.decrementLevel("blue")
                self.incrementLevel("red")
            else:
                self.fadeState = 3
        if self.fadeState == 3:
            if self.redLevel > 50:
                self.incrementLevel("green")
                self.incrementLevel("blue")
                self.decrementLevel("red")
            else:
                self.fadeState = 4
        elif self.fadeState == 4:
            if self.redLevel > 0:
                self.decrementLevel("green")
                self.incrementLevel("blue")
                self.decrementLevel("red")
            else:
                self.fadeState = 5
        if self.fadeState == 5:
            if self.blueLevel > 50:
                self.incrementLevel("green")
                self.decrementLevel("blue")
                self.incrementLevel("red")
            else:
                self.fadeState = 6
        elif self.fadeState == 6:
            if self.blueLevel > 0:
                self.incrementLevel("green")
                self.decrementLevel("blue")
                self.decrementLevel("red")
            else:
                self.fadeState = 1

    def fade4(self):
        if self.fadeState == 0:

            self.blueLevel = 100
            self.redLevel = 100
            self.greenLevel = 0

            self.fadeState = 1
        if self.fadeState == 1:
            if self.greenLevel < 100:
                self.incrementLevel("green")
                self.decrementLevel("red")
            else:
                self.fadeState = 2
        if self.fadeState == 2:
            if self.redLevel < 100:
                self.incrementLevel("red")
                self.decrementLevel("blue")
            else:
                self.fadeState = 3
        if self.fadeState == 3:
            if self.blueLevel < 100:
                self.incrementLevel("blue")
                self.decrementLevel("green")
            else:
                self.fadeState = 1

    def fade5(self):
        if self.fadeState == 0:

            self.blueLevel = 0
            self.redLevel = 100
            self.greenLevel = 0

            self.fadeState = 1
        if self.fadeState == 1:
            if self.blueLevel < 100:
                self.incrementLevel("blue")
            else:
                self.fadeState = 2
        if self.fadeState == 2:
            if self.redLevel > 0:
                self.decrementLevel("red")
            else:
                self.fadeState = 3
        if self.fadeState == 3:
            if self.redLevel < 100:
                self.incrementLevel("red")
            else:
                self.fadeState = 4
        if self.fadeState == 4:
            if self.blueLevel > 0:
                self.decrementLevel("blue")
            else:
                self.fadeState = 1




