#! /usr/bin/python
# -*-coding:utf-8 -*

from time import localtime, strftime
from os import uname 
from os.path import join
from subprocess import check_output

def get_device(path):
	device = str(check_output(["grub-probe", "--target=device", "/"]), "utf-8").strip("\n") 
	return device

date = strftime("%Y-%m-%d_%H:%M", localtime())
btrfs_device = get_device("/")
btrfs_mount_point="/media/btrfs-root"
machine = uname()[4]
main_system_dir = "manjaro_"+machine
snapshot_dir = "manjaro_"+machine+"_snapshots"
snapshot_dir_path = join(btrfs_mount_point, snapshot_dir)
main_system_dir_path = join(btrfs_mount_point, main_system_dir)
snap_ver_file = "snapshot-version"
snap_ver_file_path = "/"+snap_ver_file
