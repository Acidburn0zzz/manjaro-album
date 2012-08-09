#! /usr/bin/python
# -*-coding:utf-8 -*

from sys import exit
from os import remove
from os.path import join
from shutil import move

from ver_file import snap_ver_file_exists, write_snap_ver_file
from btrfs_root import mount_btrfs_root, umount_btrfs_root 
from snapshots import create_snapshot, delete_snapshot
from boot_folder import copy_vmlinuz_and_initramfs, move_vmlinuz_and_initramfs
from grub import update_grub

from var import *

def make_snap():
	# exit if we are already in a snapshot
	if snap_ver_file_exists() is True:
		with open(snap_ver_file_path, "r") as ver_file:
			ver = ver_file.read()
		print("""You are already in the snapshot {}.
You can't create a snapshot.""".format(ver))
		exit(1)

	# mount the root of the btrfs volume
	mount_btrfs_root()

	# create the snapshot
	snap_ver = "snapshot_"+date
	snap_path = join(snapshot_dir_path, snap_ver)
	create_snapshot(main_system_dir_path, snap_path)

	# copy initramfs and vmlinuz to the snapshot
	copy_vmlinuz_and_initramfs("/boot", snap_path+"/boot")

	# write a file to know the snapshot version
	write_snap_ver_file(snap_path, snap_ver)

	# umount the root of the btrfs volume
	umount_btrfs_root()

	# update grub.cfg file to be able to boot to the new created snapshot
	update_grub()


def make_rollback():
	# exit if we are not in a snapshot
	if snap_ver_file_exists() is False:
		print("""You are not in a recognised snapshot.
You must boot into a snapshot to rollback your system.""")
		exit(1)

	# define snap_ver from snap_ver_file
	with open(snap_ver_file_path, "r") as ver_file:
		snap_ver = ver_file.read()
	snap_path = join(snapshot_dir_path, snap_ver)

	# mount the root of the btrfs volume
	mount_btrfs_root()

	# snapshot the main system so the user can roll back to it
	# even after have done a rollback to the current snapshot
	main_system_dir_backup_path = join(snapshot_dir_path, "before-rollback-to-"+snap_ver)
	create_snapshot(main_system_dir_path, main_system_dir_backup_path)

	# move initramfs and vmlinuz to the old main system /boot directory
	move_vmlinuz_and_initramfs("/boot", main_system_dir_backup_path+"/boot")

	# write a file to the recently moved system to be recognised as a snapshot
	snap_ver_new = "snapshot_"+date
	write_snap_ver_file(main_system_dir_backup_path, snap_ver_new)

	# roll back the system by creating a new snapshot from the snapshot to the main system
	delete_snapshot(main_system_dir_path)
	create_snapshot(snap_path, main_system_dir_path)

	# erase the snapshot-version file copied in the main system
	remove(main_system_dir_path+snap_ver_file_path)

	# copy initramfs and vmlinuz from the snapshot to real /boot
	copy_vmlinuz_and_initramfs(snap_path+"/boot", "/boot")

	# umount the root of the btrfs volume
	umount_btrfs_root()

	# update grub.cfg file
	update_grub()

