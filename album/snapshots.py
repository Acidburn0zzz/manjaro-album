#! /usr/bin/python
# -*-coding:utf-8 -*

from subprocess import call, check_output
from os import mkdir
from os.path import join, isdir
from sys import exit

from album.btrfs_root import mount_btrfs_root, umount_btrfs_root
from album.grub import update_grub

from album.var import snapshot_dir_path, snapshot_dir

def create_snapshot(dir_path, snap_path):
	if isdir(snapshot_dir_path) is False:
		mkdir(snapshot_dir_path)
	call(["btrfs", "subvolume", "snapshot", dir_path, snap_path])

def delete_snapshots(name_list):
	for snap_name in name_list:
		call(["btrfs", "subvolume", "delete", join(snapshot_dir_path, snap_name)])

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
		i += 1
	return full_list

def print_snapshots_list():
	print("	number		name")
	print("	------		----")
	for number, name in list_snapshots().items():
		print("	{}		{}".format(number, name))
		#print("	--		-------------------------")

def prompt_delete_snapshots():
	snapshots_list = list_snapshots()
	delete_list = []
	selec_numbers = input("""Enter the number(s) of the snapshot you want to delete
separated by commas: """)
	selec_numbers = selec_numbers.split(",")
	for number in selec_numbers:
		try:
			number = int(number)
			delete_list.append(snapshots_list[number])
		except ValueError:
			print("Unrecognised number(s)")
			exit(1)
		except KeyError:
			print("Some numbers don't exist")
			exit(1)
	print("Here are the snapshot(s) you want to delete:")
	for name in delete_list:
		print("  * "+name)
	decision = input("Are you sure ? [y/N]: ")
	if decision.lower() == "y":
		mount_btrfs_root()
		delete_snapshots(delete_list)
		umount_btrfs_root()
		update_grub()
	else:
		exit(1)

