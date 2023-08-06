#!/usr/bin/env python3

import insteontcp
import time

def echo_it(data):
    print(binascii.hexlify(bytearray(data)))
    print("")

x = insteontcp.InsteonTCP('10.1.1.47', 9761, echo_it, echo_it)

x.turn_on('428517')
x.turn_on('41E3C4')

time.sleep(3)

x.turn_off('428517')
x.turn_off('41E3C4')

while 1:
    time.sleep(1)




# Publish to pypi command:
# python3 setup.py sdist bdist_wheel upload