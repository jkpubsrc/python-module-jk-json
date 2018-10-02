#!/usr/bin/env python3


import binascii

binData = binascii.unhexlify("D83D")
print(binData.decode("utf-16"))



