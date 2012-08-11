#! /usr/bin/python
# -*-coding:utf-8 -*

from subprocess import call

from album.ver_file import snap_ver_file_exists

from album.var import main_system_dir, btrfs_device, btrfs_mount_point

def update_grub():
	if snap_ver_file_exists() is False:
		call(["update-grub"])
	else:
		call(["mount", "-o", "subvol="+main_system_dir, btrfs_device, btrfs_mount_point])
		call(["mount", "--bind", "/boot", btrfs_mount_point+"/boot"])
		call(["mount", "-t", "sysfs", "sysfs", btrfs_mount_point+"/sys"])
		call(["mount", "-t", "proc", "proc", btrfs_mount_point+"/proc"])
		call(["mount", "-o", "bind", "/run", btrfs_mount_point+"/run"])
		call(["mount", "-o", "bind", "/dev", btrfs_mount_point+"/dev"])
		call(["chroot", btrfs_mount_point, "update-grub"])
		call(["umount", btrfs_mount_point+"/dev"])
		call(["umount", btrfs_mount_point+"/run"])
		call(["umount", btrfs_mount_point+"/proc"])
		call(["umount", btrfs_mount_point+"/sys"])
		call(["umount", btrfs_mount_point+"/boot"])
		call(["umount", btrfs_mount_point]) 

# test
if __name__ == "__main__":
	update_grub()
