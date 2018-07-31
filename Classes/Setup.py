import os
from os.path import isdir, expanduser

home = expanduser("~")
path_root = home + '/.inception/'
path_payload_enc = path_root + 'payloads/'
path_payload_raw = path_root + 'payloads_raw/'

#check the directory structure exists
def Check():
	check_path = os.path.isdir(path_root)
	check_payload = os.path.isdir(path_payload_enc)
	check_payload_raw = os.path.isdir(path_payload_raw)
	return check_path and check_payload and check_payload_raw

#create the directory structure
def Create():
	try:
		if not os.path.isdir(path_root):
			os.makedirs(path_root)
		if not os.path.isdir(path_payload_enc):
			os.makedirs(path_payload_enc)
		if not os.path.isdir(path_payload_raw):
			os.makedirs(path_payload_raw)
	except:
		raise

