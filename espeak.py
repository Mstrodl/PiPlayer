#!/usr/bin/env python3

from os import system

def synth(sentence):
    system("espeak '" + sentence + "'")