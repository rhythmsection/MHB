import fingerprint
import sys
import model
import base_app
import pickle
import os
import subprocess

# filename1 = sys.argv[1]
# filename2 = sys.argv[2]
session = model.connect()

'''this thing is not doing a thing why is it not doing a thing???!!!'''

def change_stereo_to_mono(filename):
	if os.path.exists("new_user_input.wav"):
		os.remove("new_user_input.wav")
	ffmpeg_command = "ffmpeg -i user_input.wav -ac 1  new_user_input.wav" 
 	f_ffmpeg=subprocess.Popen(ffmpeg_command, shell=True)
  	return

def compare_fingerprint_to_database(filename):
	file1 = fingerprint.main(filename)
	fingerprints = session.query(model.Fingerprint)
	counter = 1
	database_iteration = []
	for row in fingerprints:
		file2 = pickle.loads(row.fingerprint)
		match_list = []
		current_song = {}
		for i in file2:
			if i in file1:
				match_list.append(i)
		current_song["matches"] = len(match_list)		
		current_song["hatches"] = len(file1)
		current_song["title"] = row.title
		current_song["artist"] = row.artist
		current_song["album"] = row.album
		if len(match_list) > len(file1) * .97:
			current_song["is_a_match"] = "Maybe"
		else:
			current_song["is_a_match"] = "No"
		database_iteration.append(current_song)
	return database_iteration


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

def main(filename):
	compare_fingerprint_to_database(filename)


