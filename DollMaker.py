#!/usr/bin/env python3

import base64
import os

curdir = os.path.dirname(os.path.realpath(__file__))

dolllist = ["/Debs/espeak_1.46.02-2_armhf.deb", "/Debs/espeak-data_1.46.02-2_armhf.deb", "/Debs/libespeak1_1.46.02-2_armhf.deb", "/Debs/libsonic0_0.1.17-1.1_armhf.deb", "/espeak.py"]

print("Creating dolls!")

for doll in dolllist:
    source = open(curdir + doll, "rb")
    output = open(curdir + doll + ".doll", "wb+")
    contents = source.read()
    source.close()
    output.write(base64.b64encode(contents))
    output.close()
    
print("Done creating dolls!")

print("Tesing dolls")

testdoll = open(curdir + "/espeak.py" + ".doll", "rb")
testraw = open(curdir + "/espeak.py" + ".doll", "rb")
testdollcontents = testdoll.read()
testrawcontents = testraw.read()
undolledcontents = base64.b64decode(testdollcontents)
output = open(curdir + "/espeak.py" + ".doll" + ".test", "wb+")
output.write(str(undolledcontents))
output.close

if undolledcontents == testrawcontents:
    print("Dolls made successfully!!")
else:
    print("Failed!!")
    print("Doll:")
    print(undolledcontents)
    print("Raw:")
    print(testrawcontents)
    
testdoll.close()
testraw.close()