import os
import fingerprint
import model
import sys
import pickle

wav_file = sys.argv[1]

session = model.connect()

#creates and stores fingerprints for individual songs. 
def load_test_data(wav_file):
	# path = r'/Users/LEO/Documents/Programming/MRS/stupid/echoprint-codegen-master/test_data'
	# for wav_file in os.listdir(path):
	song_fingerprint = fingerprint.main(wav_file)
	pickled_song_fingerprint = pickle.dumps(song_fingerprint)
	song = model.Fingerprint(fingerprint = pickled_song_fingerprint)
	session.add(song)
	session.commit()

#new database of hashes and shit
def oh_god_this_database(wav_file):
	song_fingerprint = fingerprint.main(wav_file)
	counter = 0
	for stupid_tuple in song_fingerprint:
		individual_hash = model.Hash(id = counter, song_id = 1, single_hash = song_fingerprint[counter][0])
		counter +=1
		session.add(individual_hash)
	session.commit()

load_test_data(wav_file)

