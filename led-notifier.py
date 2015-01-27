#!/usr/bin/env python

# Import feedparser so we can easily get data from the gmail feed
import feedparser

# Import wiringpi2 which will be known as 'ledborg'!
import wiringpi2 as ledborg

# Import time so we can 'sleep' when flashing the LED
import time

# Enter your gmail username and password below
# ****** WARNING!!! Remember that anyone who can view this file can see your gmail username/password
username = "yourusername"
password = "yourpassword"

# Initialise wiringPi
ledborg.wiringPiSetup()
red_led = 0
green_led = 2
blue_led = 3
# delay when 'flashing' a sequence of colours
flash_delay = 0.25
# how many repetitions of the sequence
sequence_length = 5

# Set pinModes
ledborg.pinMode(red_led, ledborg.GPIO.OUTPUT)
ledborg.pinMode(green_led, ledborg.GPIO.OUTPUT)
ledborg.pinMode(blue_led, ledborg.GPIO.OUTPUT)
  
# This function sets the rgb values of the ledborg
# Values can be 0 or 1 (if you want to set brightness levels see https://www.piborg.org/ledborg/lesson/5)
def SetLEDValues(red_value, green_value, blue_value):
    ledborg.digitalWrite(red_led, red_value)
    ledborg.digitalWrite(green_led, green_value)
    ledborg.digitalWrite(blue_led,  blue_value)

# Set an LED using the name of a colour
def SetLEDByName(name_value):
    if (name_value == 'blue'):
         SetLEDValues(0, 0, 1)
    if (name_value == 'red'):
         SetLEDValues(1, 0, 0)
    if (name_value == 'magenta'):
         SetLEDValues(1, 0, 1)
    if (name_value == 'green'):
         SetLEDValues(0, 1, 0)
    if (name_value == 'cyan'):
         SetLEDValues(0, 1, 1)
    if (name_value == 'yellow'):
         SetLEDValues(1, 1, 0)
    if (name_value == 'white'):
         SetLEDValues(1, 1, 1)

# This function turns off the ledborg
def LEDOff():
    SetLEDValues(0, 0, 0)

# Given a string eg. 'red:green:yellow' will repeat the sequence as many times as defined by 'sequence_length'
def LEDSequence(sequence):
    sequence_list = sequence.split(':')
    for i in range(sequence_length):
        for item in sequence_list:
            SetLEDByName(item)
            time.sleep(flash_delay)

# Get the gmail atom feed (for a gmail label if specified) and parse the result, return the 'fullcount' value (the total number of unread emails)
def getMailCount(label=''):
    return int(feedparser.parse("https://" + username + ":" + password + "@mail.google.com/gmail/feed/atom/" + label)["feed"]["fullcount"])

# We could get the inbox email count later in the script but getting it here means there's no delay in the second part
print ('Get the number of emails in the inbox')
mailcount = getMailCount()
print ('New email count for inbox is ' + str(mailcount))

#
# The first part of the notification - check each label (in 'labels') and if there are new emails with that label, show a sequence of colours
#

# Define the labels you want to check here - led will flash if at least one new email is found with the specified label
#
# For example to flash red/green/white when a new email arrives with the 'work' label..
# ..followed by flashing magenta/cyan when a 'family' email arrives..
# labels = {'work':'red:green:white', 'family':'magenta:cyan'}
#
# To disable 'label' notifications just specify an empty list

labels = {}
print('Check number of emails for each label - if any...')

# iterate through the list
for label in labels.iterkeys():
    # for this label get the email count
    print ('Checking for emails with label: "' + label + '"')
    labelmailcount = getMailCount(label)
    print ('New email count for "' + label + '" is: ' + str(labelmailcount))
    # if more than 0 run the sequence of colours
    if labelmailcount > 0:
        print ('Display LED sequence: ' + labels[label])
        LEDSequence(labels[label])
	LEDOff()

#
# The second part - get the total number of unread emails in the inbox and show a colour that indicates the number
# blue = 1 email : red = 2 emails : magenta = 3 : green = 4 : cyan = 5 : yellow = 6 : white = 7 or more
#
# This time we will leave the led switched on so it continues to show the current number of new emails after the script is done
#

# show the number of emails using a colour... the led will stay on after the script is done
if mailcount > 0 :
    print('Display inbox email count')
    if mailcount == 1 : 
        output = 'blue'
    elif mailcount == 2 :         
        output = 'red'
    elif mailcount == 3 :
        output = 'magenta'
    elif mailcount == 4 :         
        output = 'green'
    elif mailcount == 5 :         
        output = 'cyan'
    elif mailcount == 6 :         
        output = 'yellow'
    elif mailcount > 6 :         
        output = 'white'
    SetLEDByName(output)
else:
    print ('No new emails - switch LED off')
    # no emails so switch led off
    LEDOff()
print ('All done :)')