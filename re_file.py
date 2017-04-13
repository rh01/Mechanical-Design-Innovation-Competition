import re

with open('file_name.txt','r') as f:
	for ii in f:
		print ii.rstrip()
		print re.findall('^.*?([0-9])',ii)[0]
		print re.findall('^.*-([0-9]+)',ii)
