#!/usr/bin/env python3

import os
import json
import socket
import threading
import sys
import time
import random

class Wpd():
	config = {}
	pictures = {}
	sock = None

	def __init__(self, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('', int(port))) # TODO: load from config
		self.load_config()
		self.load_pictures()

	def load_config(self):
		with open("./config.json","r") as f:
			self.config = json.loads(f.read())

	def load_pictures(self):
		try:
			with open("./pictures.json","r") as f:
				self.pictures = json.loads(f.read())["pictures"]
			print("loaded pictures")
		except:
			print("pictures.json not found")

	def _autopicload(self):
		while True:
			time.sleep(self.config["reload_pictures"])
			self.load_pictures()	

	def write_pictures(self):
		with open("./pictures.json","w") as f:
			json.dump(self.pictures, f, sort_keys=True, indentr=4)

	def run(self):
		self.sock.listen(5)

		picthread = threading.Thread(target=self._autopicload)
		picthread.daemon = True
		picthread.start()

		while True:
			cs, addr = self.sock.accept()
			print("received connection")
			threading.Thread(target=self.handle_request,args=(cs,addr)).start()
		# TODO: Run basic crap, start threads, loop, etc

	def get_image(self):
		# TODO: Make this better
		ind = random.randint(0,len(self.pictures)-1)
		print("Picked " + str(ind))
		with open(self.config["base_dir"] + "/" + self.pictures[ind]["name"],"rb") as f:
			ret = f.read()
		return ret

	def handle_request(self, csock, addr):
		text = csock.recv(200)
		print("received message from {} : {}".format(str(addr), str(text)))
		if text.decode("utf-8").startswith("GET"):
			csock.sendall(self.get_image())
		csock.close()

def main():
	wpd = Wpd(sys.argv[1] if len(sys.argv) == 2 else 12345)
	wpd.run()

if __name__ == "__main__":
	main()
