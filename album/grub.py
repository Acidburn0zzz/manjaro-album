#! /usr/bin/python
# -*-coding:utf-8 -*

from subprocess import call
from subprocess import PIPE as subprocessPIPE

def update_grub():
	print("Updating grub.cfg...")
	call(["update-grub"], stdout=subprocessPIPE, stderr=subprocessPIPE) 

# test
if __name__ == "__main__":
	update_grub()
