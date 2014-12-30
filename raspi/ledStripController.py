import time
import RPi.GPIO as GPIO
import requests
import os


class ledStripController(object):
    def __init__(self):
        self.RED_PIN = 11 #Change me to the pin hooked up to red
        self.BLUE_PIN = 12 #Blue pin
        self.GREEN_PIN = 13 #Green pin

        self.dataCheckFrequency = 1 #How often to check the data file, in Hertz

        self.onFrequency = 50 #in Hertz; shouldn't change
        self.strobeFrequency = .5 #baseline strobe frequency in Hz (if strobe slider was set to 0); also shouldn't change

        self.offDutyCycle = 0

        self.incrementStep = 5 #increment step for fades

        self.sampleDataString = "color 20 35 30 setting 0 brightness 23 speed 45 strobe 32 on power on"

        GPIO.setmode(GPIO.BOARD) #change if necessary

        #Setting up pins as output pins
        GPIO.setup(RED_PIN, GPIO.OUT)
        GPIO.setup(BLUE_PIN, GPIO.OUT)
        GPIO.setup(GREEN_PIN, GPIO.OUT)

        self.pwmRed = GPIO.PWM(RED_PIN, onFrequency)
        self.pwmBlue = GPIO.PWM(BLUE_PIN, onFrequency)
        self.pwmGreen = GPIO.PWM(GREEN_PIN, onFrequency)

        self.pwmRed.start(0) #starting off at 0 duty cycle
        self.pwmGreen.start(0)
        self.pwmBlue.start(0)

        self.powerOn = true
        self.strobeOn = false
        self.strobeSpeed = 50
        self.fadeSpeed = 50
        self.brightness = 50
        self.userSetting = 0
        self.reportedRedLevel = 50
        self.reportedGreenLevel = 50
        self.reportedBlueLevel = 50
        self.redLevel = 50
        self.greenLevel = 50
        self.blueLevel = 50

        self.currentTime = time.time()

        self.strobeTime = time.time()
        self.fadeTime = time.time()
        self.lastDataCheckTime = time.time()

        self.fadeState = 0

        self.checkDataFileAndUpdate()

    def runMainLoop(self):
        while true:
            self.currentTime = time.time()

            if (self.currentTime - self.lastDataCheckTime) > (1.0/float(self.dataCheckFrequency)):
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
                    if (self.currentTime - self.strobeTime)<(.5/float(self.strobeFrequency*(self.strobeSpeed + 1.0))):
                        turnAllOn()
                    elif (self.currentTime - self.strobeTime)>(1.0/float(self.strobeFrequency*(self.strobeSpeed + 1.0))):
                        self.strobeTime = self.currentTime
                    else:
                        self.turnAllOff()
            else:
                self.turnAllOff()

    def turnAllOff(self):
        """
        turn off all LED's by setting duty cycle to 0
        """
        self.pwmRed.ChangeDutyCycle(offDutyCycle)
        self.pwmGreen.ChangeDutyCycle(offDutyCycle)
        self.pwmBlue.ChangeDutyCycle(offDutyCycle)

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
        if self.setting == 1:
            fade1()

    def incrementLevel(self, colorToIncrement):
        """
        increases colorToIncrement by incrementStep defined in init

        colorToIncrement - string that corresponds to the color needed: "red", "green", or "blue"
        """
        self.changeLevel(colorToIncrement, self.incrementStep)

    def decrementLevel(self, colorToDecrement):
        """
        decreases colorToDecrement by incrementStep defined in init

        colorToDecrement - string that corresponds to the color needed: "red", "green", or "blue"
        """
        self.changeLevel(colorToDecrement, -1*self.incrementStep)

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
        response = requests.get('http://YourWebsite.com/test.php')

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

