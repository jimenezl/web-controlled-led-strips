Web controlled LED Strips on a Raspberry Pi
=========================

What is this?
------------------------
This repo contains all the code needed to be able to control your LED strips from a web page served by the Pi, with some minimal tweaking. At some point, screenshots and pictures will be uploaded. While this should work pretty much straight up out of the box, I can't make any guarantees.

Setup and Installation
-------------------------

###0. Requirements:
You'll need your Pi to have some sort of server software (for example Apache) and PHP installed. Here's a quick guide to setting both up: 
http://www.raspberrypi.org/documentation/remote-access/web-server/apache.md

Quick bash line that will install Apache and PHP:

```bash
sudo apt-get install apache2 php5 libapache2-mod-php5 -y
```

###1. Get the Code
Pull the code from the repo using your favourite method. For example, if you have git installed on your Pi:

```bash
cd /var/www/
sudo git clone https://github.com/jimenezl/web-controlled-led-strips.git ledController
```

Run the above commands to pull the code to the default Apache web folder, or get the code some other way.
Make sure it is running by going to http://localhost/ledController/server/ and confirming the controller interface loads.
Playing around with the buttons and sliders should make the values change at http://localhost/ledController/server/displayData.php 
If the values at displayData.php don't change, you might have to fiddle around with giving www-data permission:

```bash
sudo chown -R www-data:www-data /var/www/ledController/server/
sudo chmod -R 770 /var/www/ledController/server/
```

###2. Hook up your LED strips

This depends on your setup, but you'll need to choose 3 pins to use as output, one each for red, green, and blue. Pictures will be uploaded at some point in the future.

###3. Modify Python File

Open up the python file at /raspi/ledStripController.py and change the pin numbers on lines 9, 10, and 11 to the corresponding pin numbers used in your setup from step 2. Save and close the file.

###4. Run The Python

Run the python file with your favourite method.
For example:

```bash
python ledController/raspi/ledStripController.py&
```


###5. Done!
You should now be able to go to http://localhost/ledController/server/ and play around with your light strips. If you know the IP address of your Pi, you can go on your home computer or phone and navigate to http://YourPiIpAddress/ledController/server/ and control your lights from there.

###6. Next Steps
You can automate your lights to, say, turn on at 8:00AM every day, with some cron jobs. 

You can automate the changing of server/data.txt, which is what the python script relies on to know how to control the lights. 
You can play around with the web controller until your lights look like you want them to, save the contents of server/data.txt to server/dataMorning.txt, and have a script with:

```bash
cp server/dataMorning.txt server/data.txt
```

This simply copies the content of dataMorning.txt to data.txt. Then set up a cron job to run the script at 8:00AM, and you have yourself an awesome alarm (strobe would work great to wake you up :P).

You can also script automatic POST requests to the server/receiving_file.php file, if you want external machines to control it. Take a look at that to see what kind of requests you'll want to use, I'll update this in the future with more detailed documentation. 

