#!/usr/bin/env python3

# This is a reference client for interacting with wpd. Not intended for mainline use.

import os, sys
import socket

if len(sys.argv) != 3:
	print("Usage: wpc.py <hostname or IP> <port>")
	exit(1)


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((sys.argv[1],int(sys.argv[2])))
s.send(b"GET")
img = b""

while True:
	bt = s.recv(2048)
	if len(bt) == 0:
		break
	img += bt

with open("image", "wb") as f:
	f.write(img)

os.system("feh --bg-scale --no-fehbg image")
