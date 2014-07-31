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

load_test_data(wav_file)



