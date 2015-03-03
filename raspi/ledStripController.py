#!/usr/bin/python
import time
##import RPi.GPIO as GPIO
#import requests
import os
import random
import pigpio

class ledStripController(object):
    def __init__(self):
        """
        Object for controlling LED Strips
        """

        self.RED_PIN = 9 #Change me to the pin hooked up to red
        self.GREEN_PIN = 27 #Green pin
        self.BLUE_PIN = 3 #Blue pin

        self.DATA_ADDRESS = '/var/www/ledController/server/data.txt' #change if different

        self.DATA_CHECK_FREQUENCY = 1 #How often to check the data file, in Hertz

        self.ON_FREQUENCY = 100 #in Hertz;
        self.STROBE_FREQUENCY = 1.5 #baseline strobe frequency in Hz (if strobe slider was set to 0);

        self.OFF_DUTY_CYCLE = 0

        self.INCREMENT_STEP = 2 #increment step for fades

##        GPIO.setmode(GPIO.BOARD) #change if necessary

##        #Setting up pins as output pins
##        GPIO.setup(self.RED_PIN, GPIO.OUT)
##        GPIO.setup(self.BLUE_PIN, GPIO.OUT)
##        GPIO.setup(self.GREEN_PIN, GPIO.OUT)

##        self.pwmRed = GPIO.PWM(self.RED_PIN, self.ON_FREQUENCY)
##        self.pwmBlue = GPIO.PWM(self.BLUE_PIN, self.ON_FREQUENCY)
##        self.pwmGreen = GPIO.PWM(self.GREEN_PIN, self.ON_FREQUENCY)
##
##        self.pwmRed.start(0) #starting off at 0 duty cycle
##        self.pwmGreen.start(0)
##        self.pwmBlue.start(0)

##        pi.set_PWM_frequency(self.RED_PIN, self.ON_FREQUENCY)
##        pi.set_PWM_frequency(self.GREEN_PIN, self.ON_FREQUENCY)
##        pi.set_PWM_frequency(self.BLUE_PIN, self.ON_FREQUENCY)

        self.pi = pigpio.pi()

        self.pi.set_PWM_range(self.RED_PIN, 100)
        self.pi.set_PWM_range(self.GREEN_PIN, 100)
        self.pi.set_PWM_range(self.BLUE_PIN, 100)

        self.pi.set_PWM_dutycycle(self.RED_PIN, 0)
        self.pi.set_PWM_dutycycle(self.GREEN_PIN, 0)
        self.pi.set_PWM_dutycycle(self.BLUE_PIN, 0)

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

	self.dataFile = open(self.DATA_ADDRESS, 'r')
	self.oldDataLine = ""

        self.checkDataFileAndUpdate()

    def runMainLoop(self):
        """
        Call this method once to start the LED strip controlling.
        """
        while True:
            self.currentTime = time.time()

            if (self.currentTime - self.lastDataCheckTime) > (1.0/float(self.DATA_CHECK_FREQUENCY)):
                self.checkDataFileAndUpdate()
                self.lastDataCheckTime = self.currentTime

            if self.powerOn:
                if self.userSetting == 0:
                    self.setBrightness(self.BLUE_PIN, float(self.reportedBlueLevel))
                    self.setBrightness(self.GREEN_PIN, float(self.reportedGreenLevel))
                    self.setBrightness(self.RED_PIN, float(self.reportedRedLevel))
                else:
                    if ((self.currentTime - self.fadeTime)<(10.0/float((self.fadeSpeed + 1.0)))):
                        pass
                    elif ((self.currentTime - self.fadeTime)>(10.0/float((self.fadeSpeed + 1.0)))):
                        self.fade(self.userSetting)
                        self.turnAllOn()
                        self.fadeTime = self.currentTime

                if self.strobeOn:
                    if (self.currentTime - self.strobeTime)<(.5/float(self.STROBE_FREQUENCY*(self.strobeSpeed + 1.0))):
                        self.turnAllOn()
                    elif (self.currentTime - self.strobeTime)>(1.0/float(self.STROBE_FREQUENCY*(self.strobeSpeed + 1.0))):
                        self.strobeTime = self.currentTime
                    else:
                        self.turnAllOff()
            else:
                self.turnAllOff()

            if self.strobeOn:
                time.sleep(.025)
            elif self.fadeState != 0:
                time.sleep(.05)
            else:
                time.sleep(.5)


    def decimalToEightBit(self, decimal):
        return float(decimal)*255.0/100.0

    def turnAllOff(self):
        """
        turn off all LED's by setting duty cycle to 0
        """
##        self.pwmRed.ChangeDutyCycle(self.OFF_DUTY_CYCLE)
##        self.pwmGreen.ChangeDutyCycle(self.OFF_DUTY_CYCLE)
##        self.pwmBlue.ChangeDutyCycle(self.OFF_DUTY_CYCLE)

        self.pi.set_PWM_dutycycle(self.RED_PIN, self.OFF_DUTY_CYCLE)
        self.pi.set_PWM_dutycycle(self.GREEN_PIN, self.OFF_DUTY_CYCLE)
        self.pi.set_PWM_dutycycle(self.BLUE_PIN, self.OFF_DUTY_CYCLE)

    def setBrightness(self, colorPin, finalBrightness):
        """
        sets brightness of an output pin by setting the pwm pin to finalBrightness*this.brightness/100 duty cycle
        """
        self.pi.set_PWM_dutycycle(colorPin, (finalBrightness*float(self.brightness)/100.0))
##        pwmColor.ChangeDutyCycle(finalBrightness*float(self.brightness)/100.0)
        #print "setting brightness: " + str(self.redLevel) + " " + str(self.greenLevel) + " " + str(self.blueLevel)

    def turnAllOn(self):
        """
        sets brightness of all output pins to their set levels (ie. "on")
        """
##        self.setBrightness(self.pwmBlue,self.blueLevel)
##        self.setBrightness(self.pwmGreen,self.greenLevel)
##        self.setBrightness(self.pwmRed,self.redLevel)
        self.setBrightness(self.BLUE_PIN,self.blueLevel)
        self.setBrightness(self.GREEN_PIN,self.greenLevel)
        self.setBrightness(self.RED_PIN,self.redLevel)


    def fade(self, setting):
        """
        performs the fade as specified by the setting
        """
        if setting == 1:
            self.fade1()
        elif setting == 2:
            self.fade2()
        elif setting == 3:
            self.fade3()
        elif setting == 4:
            self.fade4()
        elif setting == 5:
            self.fade5()
        elif setting == 6:
            self.fade6()

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
        #dataRequest = requests.get(self.DATA_URL)
        #dataText = dataRequest.text

	self.dataFile.seek(0)
	newDataLine = self.dataFile.readline()

	if self.oldDataLine != newDataLine:
		self.oldDataLine = newDataLine
	        splitData = newDataLine.strip().split()
	        if len(splitData) == 15:
	            #print "reading: "
		    #print splitData

	            self.reportedRedLevel = float(splitData[1])
	            self.reportedGreenLevel = float(splitData[2])
	            self.reportedBlueLevel = float(splitData[3])

		    #print "red level: " + str(self.reportedRedLevel)
	            #print "green level: " + str(self.reportedGreenLevel)
	            #print "blue level: " + str(self.reportedBlueLevel)

	            self.brightness = float(splitData[7])
	            self.fadeSpeed = float(splitData[9])
	            self.strobeSpeed = float(splitData[11])

	            if splitData[12] == "on":
	                self.strobeOn = True
	            else:
	                self.strobeOn = False

	            if splitData[14] == "on":
	                self.powerOn = True
	            else:
	                self.powerOn = False

	            if self.userSetting != float(splitData[5]):
	                self.userSetting = float(splitData[5])
			#print "user setting: " + str(self.userSetting)
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

    #Random fade
    def fade6(self):
        """
        Fades in between 3 randomly chosen colors
        """

        randomColor1 = [0,0,0] # First element is level of red (0-100), second is green, third is blue
        randomColor2 = [0,0,0]
        randomColor3 = [0,0,0]
        #TODO: make a color class and replace these ^^

        minColorLevel = 0
        maxColorLevel = 20

        if self.fadeState == 0:
            #generating and assigning random colors
            randomColor1[0] = random.randint(minColorLevel,maxColorLevel) * self.INCREMENT_STEP #we want the range to be between 50 and 100, in increments of INCREMENT_STEP so we can use decrementLevel and incrementLevel
            randomColor1[1] = random.randint(minColorLevel,maxColorLevel) * self.INCREMENT_STEP
            randomColor1[2] = random.randint(minColorLevel,maxColorLevel) * self.INCREMENT_STEP

            randomColor2[0] = random.randint(minColorLevel,maxColorLevel) * self.INCREMENT_STEP
            randomColor2[1] = random.randint(minColorLevel,maxColorLevel) * self.INCREMENT_STEP
            randomColor2[2] = random.randint(minColorLevel,maxColorLevel) * self.INCREMENT_STEP

            randomColor3[0] = random.randint(minColorLevel,maxColorLevel) * self.INCREMENT_STEP
            randomColor3[1] = random.randint(minColorLevel,maxColorLevel) * self.INCREMENT_STEP
            randomColor3[2] = random.randint(minColorLevel,maxColorLevel) * self.INCREMENT_STEP

            self.redLevel = randomColor1[0]
            self.greenLevel = randomColor1[1]
            self.blueLevel = randomColor1[2]

            self.fadeState = 1

        if self.fadeState == 1:
            redError = self.redLevel - randomColor2[0]
            greenError = self.greenLevel - randomColor2[1]
            blueError = self.blueLevel - randomColor2[2]

            if ((redError != 0)):
                self.changeLevel("red", (-1*redError/abs(redError))*self.INCREMENT_STEP)
            if ((greenError != 0)):
                self.changeLevel("green", (-1*greenError/abs(greenError))*self.INCREMENT_STEP)
            if ((blueError != 0)):
                self.changeLevel("blue", (-1*blueError/abs(blueError))*self.INCREMENT_STEP)

            if (((redError == 0)) and ((greenError == 0)) and ((blueError == 0))):
                self.fadeState = 2

        if self.fadeState == 2:
            redError = self.redLevel - randomColor3[0]
            greenError = self.greenLevel - randomColor3[1]
            blueError = self.blueLevel - randomColor3[2]

            if ((redError != 0)):
                self.changeLevel("red", (-1*redError/abs(redError))*self.INCREMENT_STEP)
            if ((greenError != 0)):
                self.changeLevel("green", (-1*greenError/abs(greenError))*self.INCREMENT_STEP)
            if ((blueError != 0)):
                self.changeLevel("blue", (-1*blueError/abs(blueError))*self.INCREMENT_STEP)

            if (((redError == 0)) and ((greenError == 0)) and ((blueError == 0))):
                self.fadeState = 3

        if self.fadeState == 3:
            redError = self.redLevel - randomColor1[0]
            greenError = self.greenLevel - randomColor1[1]
            blueError = self.blueLevel - randomColor1[2]

            if ((redError != 0)):
                self.changeLevel("red", (-1*redError/abs(redError))*self.INCREMENT_STEP)
            if ((greenError != 0)):
                self.changeLevel("green", (-1*greenError/abs(greenError))*self.INCREMENT_STEP)
            if ((blueError != 0)):
                self.changeLevel("blue", (-1*blueError/abs(blueError))*self.INCREMENT_STEP)

            if (((redError == 0)) and ((greenError == 0)) and ((blueError == 0))):
                self.fadeState = 1

controller = ledStripController()
controller.runMainLoop()




