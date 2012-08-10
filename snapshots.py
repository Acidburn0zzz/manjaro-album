#! /usr/bin/python
# -*-coding:utf-8 -*

from subprocess import call, check_output
from os import mkdir
from os.path import join
from sys import exit

from btrfs_root import mount_btrfs_root, umount_btrfs_root
from grub import update_grub

from var import snapshot_dir_path, snapshot_dir

def create_snapshot(dir_path, snap_path):
	if isdir(snapshot_dir_path) is False:
		mkdir(snapshot_dir_path)
	call(["btrfs", "subvolume", "snapshot", dir_path, snap_path])

def delete_snapshot(snap_path):
	call(["btrfs", "subvolume", "delete", snap_path])

def list_snapshots():
	first_list = str(check_output(["btrfs", "subvolume", "list", "/"]), "utf-8").split("\n")
	snapshots_list = []
	for line in first_list:
		if snapshot_dir in line:
			details = line.split( )
			snap_long_name = details[6]
			lenght = len(snapshot_dir) 
			snap_name = snap_long_name[lenght+1:]
			snapshots_list.append(snap_name)
	full_list = {}
	i = 1
	for snap_name in snapshots_list:
		full_list[i] = snap_name
		i = i + 1
	return full_list

def print_snapshots_list():
	print("	number		name")
	print("	------		----")
	for number, name in list_snapshots().items():
		print("	{}		{}".format(number, name))
		#print("	--		-------------------------")

def prompt_delete_snapshot():
	snapshots_list = list_snapshots()
	selec_number = input("Enter the number of the snapshot you want to delete: ")
	try:
		selec_number = int(selec_number)
		snap = snapshots_list[selec_number]
	except ValueError:
		print("Unrecognised number")
		exit(1)
	except KeyError:
		print("This snapshot number doesn't exist")
		exit(1)
	decision = input("Are you sure you want to delete {} ? [y/N]: ".format(snap))
	if decision.lower() == "y":
		mount_btrfs_root()
		delete_snapshot(join(snapshot_dir_path, snap))
		umount_btrfs_root()
		update_grub()
	else:
		exit(1)

