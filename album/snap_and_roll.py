#! /usr/bin/python
# -*-coding:utf-8 -*

from subprocess import call
from subprocess import PIPE as subprocessPIPE
from sys import exit
from os import remove
from os.path import join
from shutil import move

from album.ver_file import snap_ver_file_exists, write_snap_ver_file
from album.btrfs_root import mount_btrfs_root, umount_btrfs_root 
from album.snapshots import create_snapshot
from album.boot_folder import copy_vmlinuz_and_initramfs, move_vmlinuz_and_initramfs
from album.grub import update_grub

from album.var import snap_ver_file_path, snapshot_dir_path, main_system_dir_path, date

def make_snap():
	if snap_ver_file_exists() is True:
		with open(snap_ver_file_path, "r") as ver_file:
			current_ver = ver_file.read()
		print("""You are already in {}.
I will create a snapshot of the current system state.""".format(current_ver))
	print("Shooting your system...")

	# mount the root of the btrfs volume
	mount_btrfs_root()

	# create the snapshot
	snap_ver = "snapshot_"+date
	snap_path = join(snapshot_dir_path, snap_ver)
	create_snapshot(main_system_dir_path, snap_path)

	# copy initramfs and vmlinuz to the snapshot
	if snap_ver_file_exists() is True:
		copy_vmlinuz_and_initramfs(join(snapshot_dir_path, current_ver)+"/boot", snap_path+"/boot")
	else:
		copy_vmlinuz_and_initramfs("/boot", snap_path+"/boot")

	# write a file to know the snapshot version
	write_snap_ver_file(snap_path, snap_ver)

	# enable the systemd service to umount boot at startup in snapshot
	call(["chroot", snap_path, "systemctl", "enable", "umountbootonsnapshot.service"], stdout=subprocessPIPE, stderr=subprocessPIPE)

	# umount the root of the btrfs volume
	umount_btrfs_root()

	# update grub.cfg file to be able to boot to the new created snapshot
	update_grub()

	print("Creation of {} successfully finished.".format(snap_ver))


def make_rollback():
	print("Rolling back your system...")

	# define snap_ver from snap_ver_file
	with open(snap_ver_file_path, "r") as ver_file:
		snap_ver = ver_file.read()
	snap_path = join(snapshot_dir_path, snap_ver)

	# mount the root of the btrfs volume
	mount_btrfs_root()

	# snapshot the main system so the user can roll back to it
	# even after have done a rollback to the current snapshot
	snap_ver_new = "snapshot_"+date
	main_system_dir_backup_path = join(snapshot_dir_path, snap_ver_new)
	create_snapshot(main_system_dir_path, main_system_dir_backup_path)

	# move initramfs and vmlinuz to the old main system /boot directory
	call(["mount", "/boot"], stdout=subprocessPIPE, stderr=subprocessPIPE)
	move_vmlinuz_and_initramfs("/boot", main_system_dir_backup_path+"/boot")

	# write a file to the recently moved system to be recognised as a snapshot
	write_snap_ver_file(main_system_dir_backup_path, snap_ver_new)

	# enable the systemd service to umount boot at startup in snapshot
	call(["chroot", main_system_dir_backup_path, "systemctl", "enable", "umountbootonsnapshot.service"], stdout=subprocessPIPE, stderr=subprocessPIPE)

	# roll back the system by creating a new main system subvolume from the snapshot
	call(["btrfs", "subvolume", "delete", main_system_dir_path], stdout=subprocessPIPE)
	create_snapshot(snap_path, main_system_dir_path)

	# erase the snapshot-version file copied in the main system
	remove(main_system_dir_path+snap_ver_file_path)

	# disable the systemd service to umount boot at startup in snapshot
	call(["chroot", main_system_dir_path, "systemctl", "disable", "umountbootonsnapshot.service"], stdout=subprocessPIPE, stderr=subprocessPIPE)

	# move initramfs and vmlinuz from the new main system to real /boot
	move_vmlinuz_and_initramfs(main_system_dir_path+"/boot", "/boot")
	call(["umount", "/boot"], stdout=subprocessPIPE, stderr=subprocessPIPE)

	# umount the root of the btrfs volume
	umount_btrfs_root()

	# update grub.cfg file
	update_grub()

	print("Your system has been successfully rolled back")
	print("For safety reason a snapshot of your system have been made before the rollback:")
	print("  * "+snap_ver_new)

def prompt_rollback():
	# exit if we are not in a snapshot
	if snap_ver_file_exists() is False:
		print("You are not in a recognised snapshot.")
		print("You must boot into a snapshot to rollback your system.")
		exit(1)
	else:
		print("Your main system will be roll back to the current state of this snapshot.")
		decision = input("Are you sure ? [y/N]: ")
		if decision.lower() == "y":
			make_rollback()

