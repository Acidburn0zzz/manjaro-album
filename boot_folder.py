#! /usr/bin/python
# -*-coding:utf-8 -*

from os import uname
from glob import glob
from shutil import copy, move

machine = uname()[4]

def list_boot(path, string):
	match_files = []
	dir_content = glob(path+"/*")
	for file in dir_content:
		if machine in file:
			if string in file:
				match_files.append(file)
	return match_files

def copy_vmlinuz_and_initramfs(boot_path, dest):
	vmlinuz_files = list_boot(boot_path, "vmlinuz")
	initramfs_files = list_boot(boot_path, "initramfs")
	for vmlinuz in vmlinuz_files:
		copy(vmlinuz, dest)
	for initramfs in initramfs_files:
		copy(initramfs, dest)

def move_vmlinuz_and_initramfs(boot_path, dest):
	vmlinuz_files = list_boot(boot_path, "vmlinuz")
	initramfs_files = list_boot(boot_path, "initramfs")
	for vmlinuz in vmlinuz_files:
		move(vmlinuz, dest)
	for initramfs in initramfs_files:
		move(initramfs, dest)

# test
if __name__ == "__main__":
	print(list_boot("/boot", "vmlinuz"))

