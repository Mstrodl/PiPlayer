#!/usr/bin/env python3

## Made by Matthew Strodl ##

from pygame import mixer # Used to play MP3s
import glob # Used to get a list of MP3s
from espeak import espeak # Used to give the user track information
from os import path # Used to get the names of tracks from the path
import random

SelectedNumber = 0
MusicLocation = "/boot/mp3/" # Sets the location to search for music. You should this to wherever your music is stored. Make sure you have a trailing slash.
MusicList = glob.glob(MusicLocation + '*.mp3') # Gets a list of all the MP3s in MusicLocation.
ScrubBackSize = 50 # The time in milliseconds to scrub backward.
ScrubForwardSize = 50 # The time in milliseconds to scrub forward

def SelectInfo(TrackNumber):
    espeak.synth("Track number " + str(TrackNumber + 1) + " selected named " + TrackName(TrackNumber) + ".") # This tells the user the name of the selected track.
    espeak.synth("Press A to play") # Tells the user how to play the selected track.

def play(TrackNumber):
    paused = 0
    mixer.init() # Starts PyGame's Mixer
    mixer.music.load(MusicList[TrackNumber]) # Load the selected MP3.
    mixer.music.play() # Plays the MP3 we just loaded.
    

def TrackName(TrackNumber):
    return path.splitext(path.basename(MusicList[TrackNumber]))[0] # Get rid of the extension and path to get the song title. For instance, '/boot/mp3/pi.mp3' gets changed to 'pi'

def MusicToggle(TrackNumber):
    if mixer.music.get_busy(): # Make sure the music is playing!
        if paused == 0: # Check if the music is paused or playing
            mixer.music.pause() # Pause the music
            paused = 1 # Set the music to paused for future reference
        elif paused == 1: # If it's not playing, unpause it!
            mixer.music.unpause() # Unpause music.
            paused = 0 # Set the music to playing for future reference
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
def PlayList(List):
    for song in List:
        track += 1
        espeak.synth("Now playing track number " + str(track + 1) + ", " + TrackName(track))
        play(track)
        while pygame.mixer.music.get_busy():
            for event in pygame.event.get():
                elif event.key == KEYLEFT:
                    MusicScrubBack()
                elif event.key == KEYRIGHT:
                    MusicScrubForward()
                elif event.key == K_a:
                    MusicToggle(SelectedNumber)
                elif event.key == K_b:
                    MusicStop()

espeak.synth("Press the left button to list all tracks, press right button to shuffle tracks, press the up button to play all tracks, move the joystick up and down to select a track, press the A button to play and pause the selected track, or move the joystick left and right to scrub forward and backward.")

#===Controls===
 
#+++Buttons+++
# Up    - Play all tracks √
# Down  - None
# Left  - List all tracks √
# Right - Shuffle
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

## START ##
# This block (marked by ## START ## and ## END ##) loops over the choices and calls their respective functions
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                if SelectedNumber <= 0:
                    espeak.synth("You're already at the top of the list!")
                elif SelectedNumber >= 1:
                    SelectedNumber -= 1
                    SelectInfo(SelectedNumber) 
            elif event.key == K_u:
                track = -1
                
            elif event.key == KEYLEFT:
                MusicScrubBack()
            elif event.key == KEYRIGHT:
                MusicScrubForward()
            elif event.key == KEYDOWN:
                if SelectedNumber <= 0:
                    espeak.synth("You're already at the bottom of the list!")
                elif SelectedNumber <= len(MusicList) - 1:
                    SelectedNumber += 1
                    SelectInfo(SelectedNumber)
            elif event.key == K_d:
                play(SelectedNumber)
            elif event.key == K_a:
                MusicToggle(SelectedNumber)
            elif event.key == K_b:
                MusicStop()
            elif event.key == K_l:
                track = -1
                for song in MusicList:
                    track += 1
                    espeak.synth("Track number " + str(track + 1) + " is " + TrackName(track) + ".")
            elif event.key == K_r:
                MusicListBAK = MusicList
                random.shuffle(MusicList)
                ShuffledList = MusicList
                MusicList = MusicListBAK
                
        elif event.type == QUIT:
            running = False
## END ##