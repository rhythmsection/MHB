import fingerprint
import sys
import model
import base_app
import pickle
import os
import subprocess
import collections

session = model.connect()


#Change the submitted .wav file from stereo (default through getUserMedia() to mono for easier fingerprinting.)
def change_stereo_to_mono(filename):
	if os.path.exists("new_user_input.wav"):
		os.remove("new_user_input.wav")
	ffmpeg_command = "ffmpeg -i user_input.wav -ac 1  new_user_input.wav" 
 	f_ffmpeg=subprocess.Popen(ffmpeg_command, shell=True)
  	return

#Takes the mono .wav file and creates a fingerprint of it, which it then compares to the existing database
#of fingerprints, returning results.
def compare_fingerprint_to_database(filename):
	file1 = fingerprint.main(filename)
	fingerprints = session.query(model.Fingerprint)
	database_iteration = []
	for row in fingerprints:
		file2 = pickle.loads(row.fingerprint)
		match_list = []
		current_song = {}
		interval_count = collections.defaultdict(int)
		interval_list = []
		for i in file2:
			for j in file1:
				if i[0] == j[0]:
					interval = i[1] - j[1]
					interval_list.append(interval_count[interval] += 1)
					match_list.append(i)
		##append dictionaries to list
		##look for max value out of all the dictionaries in list


		current_song["matches"] = len(match_list)		
		current_song["hashes"] = len(file1)
		current_song["title"] = row.title
		current_song["artist"] = row.artist
		current_song["album"] = row.album
		if len(match_list) > len(file1) * .97:
			current_song["is_a_match"] = "Maybe"
		else:
			current_song["is_a_match"] = "No"
		database_iteration.append(current_song)
	return database_iteration

def main(filename):
	compare_fingerprint_to_database(filename)


