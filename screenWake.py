#Libraries
import RPi.GPIO as GPIO
import subprocess
import tkinter
import time



#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 23

 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)




def checkTimer(timeUp):
    timeUp += 1
    if timeUp > 18000:
        return -1
    else:
        return timeUp

def notAFK(object, time):
    global afk
    
    object.destroy()
    afk = 0
    time = 0
    return time

 
        
def distance():
    print("Measuring distance...")
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    print("Complete")
    return distance


 
def main(minDist):
    try:
        # Initialize: Screen-Off
        global afk
        afk = 1
        subprocess.call('XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset dpms force off', shell=True)
        print('Screen Off')
        screenActive = False
        timeUp = 0
        
        while True:

            if screenActive is False:
                dist = distance()
            elif screenActive is True:
                ## Disable checks on distance.
                dist = minDist
                ## Iterate timer
                timeUp = checkTimer(timeUp)
                ## If it has been 5 hours
                if timeUp is -1:
                    checkAFK = tkinter.Tk()
                    checkAFK.title("AFK")
                    checkAFK.minsize("500x500")
                    checkAFK.button = tkinter.Button(text='Are you there?', command=lambda: notAFK(checkAFK, timeUp), padx=100, pady=100)
                    checkAFK.button.pack()
                    if afk == 1:
                        subprocess.call('XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset dpms force off', shell=True)
                        screenActive = False
                    
                
            ## Three distance checks to eliminate false positives
            if dist < minDist and screenActive is False:
                time.sleep(0.25)
                dist = distance()
                
                if dist < minDist:
                    time.sleep(0.25)
                    dist = distance()
                    
                    # Screen-On
                    if dist < minDist:
                        subprocess.call('XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset dpms force on', shell=True)
                        print('Screen Active')
                        screenActive = True
            
                
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            
                
 
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

def setDistWindow():
    ## SelectDistance Window
    selectDist = tkinter.Tk()
    selectDist.minsize('100x100')
    selectDist.dist = tkinter.Label(selectDist, text='Enter Minimum Distance: ')
    selectDist.enterDist = tkinter.Entry(selectDist)
    selectDist.done = tkinter.Button(selectDist, text='Done', command=lambda: setDist(selectDist))

    ## Pack window
    selectDist.dist.grid(row = 1, column = 1)
    selectDist.enterDist.grid(row = 1, column = 1)

def setDist(window):
    global minDist
    minDist = 40
    minDist = window.enterDist.get()


if __name__ == '__main__':
    print("Running...")
    setDistWindow()
    main(minDist)
        


