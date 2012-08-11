#! /usr/bin/python
# -*-coding:utf-8 -*

from subprocess import call
from os.path import isdir
from os import mkdir

from album.var import btrfs_device, btrfs_mount_point

def mount_btrfs_root():
	if isdir(btrfs_mount_point) is False:
		mkdir(btrfs_mount_point)
	call(["mount", btrfs_device, btrfs_mount_point])

def umount_btrfs_root():
	call(["umount", btrfs_mount_point])

