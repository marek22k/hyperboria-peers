#!/usr/bin/env python3
"""Ping nodes and show unavailable."""
import json
import os
import sys
import subprocess
import re

RED    = '\x1b[01;31m'
GREEN  = '\x1b[01;32m'
YELLOW = '\x1b[01;33m'
END    = '\x1b[0m'


def validate(path):
	"""Test a single set of peering creds."""
	result = True
	print("Pinging %s" % path)
	try:
		with open(path) as f:
			for host in json.loads(f.read()):
				ip = ""
				indices = [i.start() for i in re.finditer(":", host)]
				if host[0] == '[':
					ip = host[1:indices[-1]-1]
				else:
					ip = host[0:indices[-1]]
				res  = subprocess.call(['ping', '-c3', '-W5', ip], stdout=subprocess.DEVNULL)
				if res:
					print("    %s%s is failed%s" % (RED, ip, END))
					result = False
				else:
					print("    %s%s is ok%s" % (GREEN, ip, END))
	except ValueError:
		print("    %sInvalid JSON!%s" % (RED, END))
		result = False
	except KeyboardInterrupt:
		print("    %sInterrupt%s" % (RED, END))
		sys.exit(1)
	return result

if __name__ == "__main__":
	success = True
	for directory, subdirs, files in os.walk('.'):
		if len(files) > 0:
			if directory != '.' and not directory.startswith('./.git'):
				for f in files:
					result = validate("%s/%s" % (directory, f))
					if not result:
						success = False
	if not success:
		sys.exit(1)
