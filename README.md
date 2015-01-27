LedBorg+Raspberry Pi Gmail Notifier
===================================

This python script uses the LedBorg add on board for Raspberry Pi to let you know how many new (unread) emails you have in your inbox. The LED stays on constantly when you have unread emails so you can always see how many new messages you have. It can also be used to check for new emails with particular labels and flash a sequence of colours when there's at least one new message with that label.

<h2>Requirements</h2>
<li>
<ul>Raspberry Pi</ul>
<ul>LedBorg add on board - you can get one from <a href="http://www.piborg.com/ledborg">PiBorg</a></ul>
<ul>Python 2.7</ul>
<ul>Feedparser module - for parsing the gmail atom feed</ul>
<ul>WiringPi2 module - controls the LED</ul>
</li>


<h2>Installation</h2>

1. You need to install the WiringPi2 and Feedparser modules<br>

    ```
    sudp apt-get update
    sudo apt-get -y install python-dev python-setuptools
    ```

    Now use easy_install to install WiringPi2 and Feedparser

    ```
    sudo easy_install wiringpi2 feedparser
    ``` 

2. Make the led-notifier.py script executable<br>

    ```
    sudo chmod +x ./led-notifier.py
    ```
    
3. Configure the login details<br>

    Edit led-notifier.py

    ```
    sudo nano led-notifier.py
    ```

    Find the following lines and change yourusername and yourpassword to your actual gmail username and password

    ```python
    username = "yourusername"
    password = "yourpassword"
    ```

    Save the changes (Ctrl-X, Y, Enter)

4. Test the script<br>

    ```
    sudo ./led-notifier.py
    ```

    If you have any unread emails in your gmail inbox the LedBorg should light up. The colour depends on how many unread emails there are.<br><br>
    1-blue 2-red 3-magenta 4-green 5-cyan 6-yellow 7-white<br><br>
    If there are no emails the LedBorg will switch off. You should also see some output from the script telling you what it is doing.<br>

5. Check for messages with a label. This step is optional. Before the script counts the unread emails in your inbox you can have it check for messages with a particular label and flash a sequence of colours that tell you at least one message has arrived with that label.<br><br>For example, you might want to flash the LedBorg red/green/yellow when a message arrives with the label 'work' or magenta/cyan when you get one with the 'payment' label. (You can apply labels to new emails based on the sender - at gmail.com look at Settings -> Filters -> Create a new filter)<br><br>
After checking for these labels and flashing the LedBorg, the default inbox check will run and a solid colour will be left on after the script ends as usual.<br>

    To configure the label-based check, find this line and edit it to your own requirements.

    ```python
    labels = {}
    ```
    eg. change this to
    
    ```python
    labels = {'work':'red:green:yellow','payment':'magenta:cyan'}
    ```
  
    You can add as many labels as you want but remember that each time the script checks for messages it will take a few seconds.
    To disable the label check completely just change the line back to:

    ```python
    labels = {}
    ```


6. Set up cron to run the script. To make the script run automatically:<br>
   
    ```
    sudo crontab -e
    ```

    Add a line to this file...

    ```
    * * * * * sudo /usr/bin/python /home/pi/ledborg-raspberrypi-gmail-notifier/led-notifier.py
    ```

    This will run the script every minute. If the script is not in the /home/pi/ledborg-raspberrypi-gmail-notifier/ directory you will need to edit the path.
    Save the changes (Ctrl-X, Y, Enter)

    The notifier will now run every minute even after a reboot.

<h2>Author</h2>

Ian Ashbury - https://github.com/ianashbury - feel free to contact me with any questions or comments at <ianashbury@gmail.com>

Based on the lessons at piborg.org - https://www.piborg.org/ledborg-new/install
