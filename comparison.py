import fingerprint
import sys

filename1 = sys.argv[1]
filename2 = sys.argv[2]

def fingerprint_both_files(filename1, filename2):
	file1 = fingerprint.main(filename1)
	file2 = fingerprint.main(filename2)
	match_list = []
	for i in file2:
		if i in file1:
			match_list.append(i)
	print "%s matches out of %s hashes." %(len(match_list), len(file2))
	if len(match_list) > (len(file2)) * .7:
		print "These are probably from the same song."
	elif len(match_list) > (len(file2)) * .4 and len(match_list) < (len(file2)) * .7:
		print "These two songs might be different."
	else:
		print "These are probably not the same song." 

def main(filename1, filename2):
	fingerprint_both_files(filename1, filename2)

main(filename1, filename2)
