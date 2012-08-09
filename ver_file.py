#! /usr/bin/python
# -*-coding:utf-8 -*

from os.path import isfile

from var import snap_ver_file_path

def snap_ver_file_exists():
	return isfile(snap_ver_file_path)

def write_snap_ver_file(path, ver):
	with open(path+snap_ver_file_path, "w") as ver_file:
		ver_file.write(ver)

