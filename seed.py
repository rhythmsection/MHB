import os
import fingprinter
import model

def load_test_data(wav_file):
	path = r'/Users/LEO/Documents/Programming/MRS/stupid/echoprint-codegen-master/test_data'
	for wav_file in os.listdir(path):
		song_fingerprint = fingerprinter.create_fingerprint(wav_file)
		pickled_song_fingerprint = pickle.dumps(song_fingerprint)
		#get song information here from song file? how do I do this?????
		song = model.Song(title = <blah>, album = <blah>, artist = <blah>, fingerprint = pickled_song_fingerprint)
		session.add(song)
		session.commit()



