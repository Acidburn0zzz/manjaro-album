#! /usr/bin/python
# -*-coding:utf-8 -*

from subprocess import call
from os import mkdir

from var import snapshot_dir_path

def create_snapshot(dir_path, snap_path):
	if isdir(snapshot_dir_path) is False:
		mkdir(snapshot_dir_path)
	call(["btrfs", "subvolume", "snapshot", dir_path, snap_path])

def delete_snapshot(snap_path):
	call(["btrfs", "subvolume", "delete", snap_path])

