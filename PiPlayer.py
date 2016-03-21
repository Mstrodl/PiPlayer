#!/usr/bin/env python3

## Made by Matthew Strodl ##

from PIL import Image
from pygame import mixer # Used to play MP3s
import glob # Used to get a list of MP3s
try:
    __import__("espeak") # Used to give the user track information
except ImportError:
    FirstRun = True
else:
    FirstRun = False
    import espeak
try:
    __import__("sense_hat") # I test my code on non-pi devices... check if it is a pi with a sense hat
except ImportError:
    import sense_hat_substitution as SenseHat
else:
    from sense_hat import SenseHat
    

from os import system # Used to run commands
from os import path # Used to get the names of tracks from the path
import random # Used to shuffle songs
#import RPi.GPIO as GPIO # used for input
from pygame.locals import * # Used for input
import pygame # Used for input
import base64 # Used to undoll the dependencies

if path.isfile("/usr/bin/espeak"): 
    FirsRun = False # The absence of doll makes me repeat this
else:
    FirstRun = True # The absence of doll makes me repeat this

system("sudo amixer cset numid=3 1") # Set audio output to analog jack
system("sudo amixer cset numid=1 100%") # Set volume to 100% then manage it with PyGame

SelectedNumber = 0 # Sets the default track
pygame.init() # Starts pygame.

pygame.mixer.music.set_volume(5 / 10) # Set the default volume (50%)


scriptfolder = path.dirname(path.realpath(__file__)) # Get directory the script lives in
Updater = True # Set this to false if you don't want the script to check for updates.
password = "raspberry" # Set this to the password of the current user
InternetAvailableInSpace = True # Set this to False if the Pi isn't connected to the internet (or you don't want song information (TODO))
MusicLocation = "/Users/matthew/Desktop/MP3/" # Sets the location to search for music. You should this to wherever your music is stored. Make sure you have a trailing slash.
MusicList = glob.glob(MusicLocation + '*.mp3') # Gets a list of all the MP3s in MusicLocation.
ScrubBackSize = 50 # The time in milliseconds to scrub backward.
ScrubForwardSize = 50 # The time in milliseconds to scrub forward
print(MusicList) # Just a little debug thingy :-).

def InstallDEB(deb):
#    system("export SUDO_ASKPASS2=$SUDO_ASKPASS; export SUDO_ASKPASS='/bin/echo " + password + "'; sudo -A dpkg -i " + deb + "; export SUDO_ASKPASS=$SUDO_ASKPASS2; unset SUDO_ASKPASS2") # This allows me to install the dependencies without a user entering the password in the terminal. # Apparanately passwords aren't needed? uncomment this if this isn't the case....

    system("cd " + deb + "; sudo cp -r usr/ /; sudo bash ./postinst configure")

def NextTrack(SelectedNumber):
    if SelectedNumber >= len(MusicList) - 1: # If the track selected is the last one.
        espeak.synth("You are already at the bottom of the list!")
    elif SelectedNumber <= len(MusicList) - 1: # If the track is not the last one
        SelectedNumber += 1 # Select the next track
        SelectInfo(SelectedNumber) # Tell the user about the track
        
def PrevTrack(SelectedNumber):
    if SelectedNumber <= 0: # If the track selected is the first
        espeak.synth("You are already at the top of the list!")
    elif SelectedNumber >= 1: # If the track selected is not the first
        SelectedNumber -= 1 # Select the previous track
        SelectInfo(SelectedNumber) # Tell the user about the track

def SelectInfo(TrackNumber):
    espeak.synth("Track number " + str(TrackNumber + 1) + " selected named " + TrackName(TrackNumber) + ".") # This tells the user the name of the selected track. TODO add audio fingerprinting with Dejavu
    espeak.synth("To play press the A, button") # Tells the user how to play the selected track.

def play(TrackNumber):
    paused = False # Set the track to be unpaused
    mixer.init() # Starts PyGame's Mixer
    mixer.music.load(MusicList[TrackNumber]) # Load the selected MP3.
    mixer.music.play() # Plays the MP3 we just loaded.
    if path.isfile(path.splitext(MusicList[TrackNumber])[0] + ".jpg"):
        im = Image.open(path.splitext(MusicList[TrackNumber])[0] + ".jpg") # Open the thumbnail 
        out = im.resize((8, 8)) # Resize the image
        sense.load_image(path.splitext(MusicList[TrackNumber])[0] + ".jpg") # Display the thumbnail on the Sense HAT
    elif path.isfile(path.splitext(MusicList[TrackNumber])[0] + ".png"):
        im = Image.open(path.splitext(MusicList[TrackNumber])[0] + ".png") # Open the thumbnail
        out = im.resize((8, 8)) # Resize the image
        sense.load_image(path.splitext(MusicList[TrackNumber])[0] + ".png") # Display the thumbnail on the Sense HAT
    else:
        sense.show_message("Now playing " + TrackName(TrackNumber)) # If the thumbnail doesn't exist, just display the name of the file
    

def TrackName(TrackNumber):
    return path.splitext(path.basename(MusicList[TrackNumber]))[0] # Get rid of the extension and path to get the song title. For instance, '/boot/mp3/pi.mp3' gets changed to 'pi'

def MusicToggle(TrackNumber):
    if mixer.music.get_busy(): # Make sure the music is playing!
        if paused: # Check if the music is paused or playing
            mixer.music.pause() # Pause the music
            paused = True # Set the music to paused for future reference
        else: # If it's not playing, unpause it!
            mixer.music.unpause() # Unpause music.
            paused = False # Set the music to playing for future reference
    else:
        play(TrackNumber) # If nothing's playing, start playnig the selected track to let this button be multifunctional.

def MusicStop():
    if mixer.music.get_busy(): # Make sure the music is playing!
        mixer.music.stop() # Stop the song that's playing.

def MusicScrubForward():
    if mixer.music.get_busy(): # Make sure the music is playing!
        MusicPosition = mixer.music.get_pos() + ScrubForwardSize # Store the position for later.
        mixer.music.rewind() # Setting the position on an MP3 file is relative. We need to rewind it first to scrub properly.
        mixer.music.set_pos(MusicPosition) # Set the position to the one we set before.

def MusicScrubBack():
    if mixer.music.get_busy(): # Make sure the music is playing!
        MusicPosition = mixer.music.get_pos() + ScrubBackSize # Store the position for later.
        mixer.music.rewind() # Setting the position on an MP3 file is relative. We need to rewind it first to scrub properly.
        mixer.music.set_pos(MusicPosition) # Set the position to the one we set before.
def PlayList(List, track):
    
    for song in List:
        track += 1 # Selects the next track
        espeak.synth("Now playing track number " + str(track + 1) + ", " + TrackName(track)) # Tells the user the playing track
        play(track) # Plays the track
        while pygame.mixer.music.get_busy(): # Loops until the music stops.
            for event in pygame.event.get(): # Loops over every event.
                if hasattr(event, 'key'): # Make sure it's a keyboard event (I had problems with it being a mouse event)
                    if event.key == pygame.K_LEFT and event.type == pygame.KEYDOWN: # If the joystick is left
                        MusicScrubBack() # Scrub backwards
                    elif event.key == pygame.K_RIGHT and event.type == pygame.KEYDOWN: # If the joystick is right
                        MusicScrubForward() # Scrub forward
                    elif event.key == pygame.K_UP and event.type == pygame.KEYDOWN: # If the joystick is up
                        MusicToggle(Track) # Toggle pause so the user can hear the info
                        if Track <= 0: # If it's the first track
                            espeak.synth("You are already at the top of the list!")
                            MusicToggle(Track)
                        elif Track > 0: # If it's not the first track
                            track -= 2 # Select the previous track. This has to be -= 2 NOT -= 1 otherwise it'll play this song over and over.
                            MusicToggle(Track) # Unpause it
                            MusicStop(Track) # Stop the music
                    elif event.key == pygame.K_DOWN and event.type == pygame.KEYDOWN: # If the joystick is up
                        MusicToggle(Track) # Pause it so the user hears the info
                        if track >= len(List) - 1: # If the track is the last one
                            espeak.synth("You are already at the bottom of the list!")
                            MusicToggle(Track) # Unpause it
                        elif Track < len(List) -1: # If the track isn't the last one
                            MusicToggle(Track) # Unpasue it
                            MusicStop() # Stop it. I don't need to do += 1 because it'll be done automatically
                    elif event.key == pygame.K_a and event.type == pygame.KEYDOWN: # If A button is pressed
                        MusicToggle(SelectedNumber) # Pause/Unpause music
                    elif event.key == pygame.K_b and event.type == pygame.KEYDOWN: # If B button is pressed
                        MusicStop() # Stop the music
                        global SelectedNumber
                        SelectedNumber = track # Set the Selected song to be the track you just stopped.
                        return # Make sure to exit the function so it doesn't play the next one....
    global SelectedNumber # Allows editing of the selected song
    SelectedNumber = track # Set the Selected song to be the track you stopped at.



#===Controls===
 
#+++Buttons+++
# Up    - Play all tracks √
# Down  - Volume √
# Left  - List all tracks √
# Right - Shuffle √
# A     - Play/Pause √
# B     - Stop √
#+++Buttons+++

#+++Joystick+++
# Up    - Select previous track √
# Down  - Select next track √
# Left  - Scrub backward √
# Right - Scrub forward √
#+++Joystick+++

#===Controls===
if FirstRun:
    print("Welcome to PiPlayer.")
    print("Please wait while we install the debs (That aren't really debs!!).")

    InstallDEB(scriptfolder + "/libsonic0/")
    InstallDEB(scriptfolder + "/espeak-data/")
    InstallDEB(scriptfolder + "/libespeak1/")
    InstallDEB(scriptfolder + "/espeak/")
    
    print("Done installing debs. (That aren't really debs.)")    
import espeak
espeak.synth("Press the left button to list all tracks, press right button to shuffle tracks, press the up button to play all tracks, press the down button to change the volume, move the joystick up and down to select a track, press the A, button to play and pause the selected track, press the B button to stop the playing track, or move the joystick left and right to scrub forward and backward.")

## START ##
# This block (marked by ## START ## and ## END ##) loops over the choices and calls their respective functions
running = True
while running:
    #pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if hasattr(event, 'key'):
            print(event)
            if event.key == pygame.K_UP and event.type == pygame.KEYDOWN: # If joystick is up
                PrevTrack(SelectedNumber) # Select the previous track
            elif event.key == pygame.K_u and event.type == pygame.KEYDOWN: # If the up button is pressed
                track = -1 # Set the track to -1 so that it starts at the 1st track. This is because at the start it'll add 1 to it so -1 will become 0 and 0 is the 1st track
                PlayList(MusicList, track) # Play the list of music in order
            elif event.key == pygame.K_LEFT and event.type == pygame.KEYDOWN: 
                MusicScrubBack()
            elif event.key == pygame.K_RIGHT and event.type == pygame.KEYDOWN:
                MusicScrubForward()
            elif event.key == pygame.K_DOWN and event.type == pygame.KEYDOWN:
                NextTrack(SelectedNumber)
            elif event.key == pygame.K_d and event.type == pygame.KEYDOWN:
                play(SelectedNumber)
            elif event.key == pygame.K_a and event.type == pygame.KEYDOWN:
                MusicToggle(SelectedNumber)
            elif event.key == pygame.K_b and event.type == pygame.KEYDOWN:
                MusicStop()
            elif event.key == pygame.K_l and event.type == pygame.KEYDOWN:
                track = -1
                for song in MusicList:
                    track += 1
                    espeak.synth("Track number " + str(track + 1) + " is " + TrackName(track) + ".")
            elif event.key == pygame.K_r and event.type == pygame.KEYDOWN:
                MusicListBAK = MusicList
                random.shuffle(MusicList)
                ShuffledList = MusicList
                MusicList = MusicListBAK
            elif event.key == pygame.K_d and event.type == pygame.KEYDOWN:
                if pygame.mixer.music.get_volume() >= 1.0:
                    pixels = sense.get_pixels()
                    sense.clear()
                    pygame.mixer.music.set_volume(0)
                    if pygame.mixer.music.get_volume() * 10 >= 10:
                        sense.show_message(str(pygame.mixer.music.get_volume() * 10))
                    elif pygame.mixer.music.get_volume() * 10 <= 9:
                        sense.show_letter(str(pygame.mixer.music.get_volume() * 10))
                    sleep(1)
                    sense.clear()
                    sense.set_pixels(pixels)
                elif pygame.mixer.music.get_volume() < 1.0:
                    pixels = sense.get_pixels()
                    sense.clear()
                    pygame.mixer.music.set_volume((pygame.mixer.music.get_volume() * 10 + 1) / 10)
                    if pygame.mixer.music.get_volume() * 10 >= 10:
                        sense.show_message(str(pygame.mixer.music.get_volume() * 10))
                    elif pygame.mixer.music.get_volume() * 10 <= 9:
                        sense.show_letter(str(pygame.mixer.music.get_volume() * 10))
                    sleep(1)
                    sense.clear()
                    sense.set_pixels(pixels)
                
## END ##