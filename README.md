# MediaServer
    ## RASPI MEDIA SERVER USER MANUAL ##

        For full functionality- You need:
            1. A Raspberry pi.
            2. A PC, windows or mac.
            3. An ultrasonic sensor, recommended: 
               https://core-electronics.com.au/hc-sr04-ultrasonic-module-distance-measuring-sensor.html
            4. A breadboard, female-male jumper cables, one 330ohm resistor, and one 470ohm resistor.

    
    ## INSTALLATION TUTORIALS ##

        - To install the ultrasonic sensor: https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
        - To install REALVNC: https://www.realvnc.com/en/


        ## ADVANCED TUTORIAL (DEVS) ##
            - To eliminate dependencies, feel free to use the .exe files instead, found here: 
              https://drive.google.com/open?id=1hr4NOvnaxfS4IS6hs6VPmC_OZlZB7JpX
            - Dependencies: Paramiko Library and Socket Library
            - Find the required programs here: https://github.com/bhodgs/MediaServer
            - Download 'sftp.py', 'screenWake.py' and 'setup.py'
            - Transfer the screenWake.py and setup.py to the Raspberry pi however you like.
            - Run setup.py, and make sure once the config menu appears, you enable VNC.
            - Restart the Pi.
            - Ensure you have the sensor setup (line 12).
            - Run screenWake.py and choose your preferred minimum distance.
            - Lastly, run sftp.py on whichever computer, and enter the user details for the SSH.
            - Default login for the raspi is: (User: pi) (Password: raspberry).
            - If the program can't find your pi, ensure you have set it up properly, and it has bee on for atleast 5 minutes                 before you connect.
            
        
        ## EASY TUTORIAL ##

            - Ensure you have the ultrasonic sensor installed (line 12).
            - Download the .exe files from this google drive: 
              https://drive.google.com/open?id=1hr4NOvnaxfS4IS6hs6VPmC_OZlZB7JpX
            - Put the 'setupAPP' and 'screenWakeAPP' folders onto your raspberry pi (would recommend just downloading them on               the pi with the link above)
            - Run the setup.exe file found within the 'dist' folder.
            - Ensure you enable the vnc once the menu comes up.
            - Restart the pi and run the screenWake.exe file, found in the 'dist' folder aswell.
            - Return to your PC and run sftp.exe in the sftpAPP/dist folder.
            - If the program can't tell you the host address, make sure your pi has been on for at least 5 minutes.
            - Enter the host address of your pi (this can also be found on your routers admin page, and will be 10.0.0.XX)
            - Default login for the raspi is: (User: pi) (Password: raspberry).
            - Your pi will now be able to receive files from your PC.
            




    
