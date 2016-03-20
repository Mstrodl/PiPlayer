#!/usr/bin/env python3

from sense_hat import SenseHat
import system from os
import sleep from time as timesleep
from pygame.locals import *
import pygame

sense = SenseHat()

sense.show_message("A = Install", text_colour=(255, 0, 0)) # Ask for confirmation before installing the dependencies.


## START ##
# This block (starting at ## START ## and ending at ## END ##) Starts the installation of the dependencies when the A button is pressed.
running = True 

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            elif event.key == K_a:
                sense.clear()
                sense.show_message("Installing deps.", text_colour=(255, 0, 0)) # Tells the user that the dependencies are installing.
                system("export SUDO_ASKPASS2=$SUDO_ASKPASS; export SUDO_ASKPASS='/bin/echo raspberry'; sudo -A dpkg -i Debs/espeak-data_1.46.02-2_armhf.deb Debs/espeak_1.46.02-2_armhf.deb Debs/libespeak1_1.46.02-2_armhf.deb Debs/libsonic0_0.1.17-1.1_armhf.deb Debs/python-espeak_0.4-1_armhf.deb; export SUDO_ASKPASS=$SUDO_ASKPASS2; unset SUDO_ASKPASS2") # Installs dependencies.
                sense.show_message("Done!", text_colour=(255, 0, 0)) # Tells the user the installation has completed.
                timesleep(5)
                running = False
        if event.type == QUIT:
            running = False
## END ##