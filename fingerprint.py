import scipy
import numpy
import collections
from scipy.io import wavfile
from numpy.fft import rfft
import math
import sys
import hashlib

# a global variable that represents the number of pockets minus one
NUM_POCKETS = 60

#tells the command line to take an argument. (the wav file)
# filename = sys.argv[1]

#slice the data from the wav file into chunks. 
def slice_some_data(filename):
	#return the rate and the amount of data as separate variables.
	rate, data = wavfile.read(filename)
	#I'm not actually sure I use this variable, but it's good to know. 
	number_of_bins = len(data/22050)
	#take the data and slice it into chunks of ___ length. 
	index = 0
	#dictionary storage of all of the data
	bins = collections.defaultdict(list)
	#slices data into subsets based on the number of Hz. Note overlap. 
	for i in range(0, len(data), 22050):
		slice = data[i:i+44100]
		#run fourier transform on each slice.
		fourier_transformed = rfft(slice)
		#assign these frequencies to bin entries in bin.
		for frequency in fourier_transformed:
			bins[index].append(frequency.real)
		index += 1
	return bins

#creates and stores frequencies from FFT into logarithmically filled pockets within each bin. 
def slice_frequencies_into_log_pockets(bin_key, bins):
	bin_location = bins[bin_key]
	max_frequencies_in_bin = []
	amplitudes_in_pocket = []
	frequencies_in_bin = []

	max_log_idx = math.log10(len(bin_location))
	pocket_size = float(max_log_idx)/NUM_POCKETS
	pockets = [ [] for x in range(NUM_POCKETS) ]
	
	for frequency, amplitude in enumerate(bin_location):
		if frequency == 0:
			continue
		log_index = math.log10(frequency)
		pocket_idx = int(log_index/pocket_size)
		pockets[min(pocket_idx, NUM_POCKETS-1)].append((abs(amplitude), frequency))
	return pockets

#finds the max of each pocket. 
def find_pocket_max(pockets):
	max_pockets = []
	for p in pockets[5:]:
		if p:
			max_pockets.append((max(p), p.index(max(p))))
	return max_pockets

#trims the actual amplitudes in each pockets to a minimum amplitude. 
def trim_minimum_amplitudes(max_pockets):
	trimmed_max_pockets = []
	min_amp = 30000.0
	for max in max_pockets:
		if max[0][0] > min_amp:
		#max frequency and index of max_frequency ala original pockets list. 
			trimmed_max_pockets.append((max[0][1], max[1]))
	return trimmed_max_pockets

# # frequency based time pairs
# def assigning_time_to_frequency_points(music_fingerprint):
# 	frequency_pair_list = []
# 	for idx, trimmed_max_pockets in enumerate(music_fingerprint):
# 		for number in trimmed_max_pockets:
# 			frequency_pair_list.append((number, idx))
# 	return frequency_pair_list

# # pocket based time pairs
# def assigning_time_to_pocket_points(music_fingerprint):
# 	frequency_pair_list = []
# 	for idx, trimmed_max_pockets in enumerate(music_fingerprint):
# 		for pocket_idx, number in enumerate(trimmed_max_pockets):
# 			frequency_pair_list.append((pocket_idx, idx))
# 	return frequency_pair_list

# pocket based time pairs redux
def assigning_time_to_pocket_points2(music_fingerprint):
	frequency_pair_list = []
	for idx, trimmed_max_pockets in enumerate(music_fingerprint):
		for frequency_tuple in trimmed_max_pockets:
			frequency_pair_list.append((frequency_tuple[1], idx))
	return frequency_pair_list

#creates locational fingerprint
def location_fingerprint(filename):
	raw_fingerprint = []
	bins = slice_some_data(filename)
	bin_count = len(bins)
	for idx, bin in enumerate(bins):
		print 'processing bin %s of %s' % (idx, bin_count)
		pockets = slice_frequencies_into_log_pockets(bin, bins)
		max_pockets = find_pocket_max(pockets)
		trimmed_max_pockets = trim_minimum_amplitudes(max_pockets)
		raw_fingerprint.append(trimmed_max_pockets)

	location_fingerprint = assigning_time_to_pocket_points2(raw_fingerprint)
	# location_fingerprint.sort()
	return location_fingerprint

#create time(bin)/frequency pairs for deeper organization. 
def fingerprint_pair_hashing(location_fingerprint):
	'''How far ahead we can look into the fingerprint to make pairs'''
	range_value = 10
	'''bin difference between pairs'''
	min_time_difference = 1
	max_time_difference = 3
	final_fingerprint = []
	fingerprinted = set()
	for i in range(len(location_fingerprint)):
		for j in range(1, range_value):
			if (i + j) < len(location_fingerprint) and not (i, i + j) in fingerprinted:
				f1 = location_fingerprint[i][0]
				f2 = location_fingerprint[i + j][0]

				t1 = location_fingerprint[i][1]
				t2 = location_fingerprint[i + j][1]

				time_difference = t2 - t1

				if time_difference >= min_time_difference and time_difference <= max_time_difference:
					h = hashlib.sha1(
						   "%s|%s|%s" % (str(f1), str(f2), str(time_difference)))
					final_fingerprint.append((h.hexdigest(), t1))	
				# print 'processing hashes %s of %s' %(i, len(location_fingerprint))
				fingerprinted.add((i, i + j))
	return final_fingerprint

# def individual_hashes(location_fingerprint):
# 	'''How far ahead we can look into the fingerprint to make pairs'''
# 	range_value = 10
# 	'''bin difference between pairs'''
# 	min_time_difference = 0
# 	max_time_difference = 3
# 	final_fingerprint = []
# 	fingerprinted = set()
# 	for i in range(len(location_fingerprint)):
# 		for j in range(1, range_value):
# 			if (i + j) < len(location_fingerprint) and not (i, i + j) in fingerprinted:
# 				f1 = location_fingerprint[i][0]
# 				f2 = location_fingerprint[i + j][0]

# 				t1 = location_fingerprint[i][1]
# 				t2 = location_fingerprint[i + j][1]

# 				time_difference = t2 - t1

# 				if time_difference >= min_time_difference and time_difference <= max_time_difference:
# 					print str(f1), str(f2), str(time_difference)
# 					h = hashlib.sha1(
# 						   "%s|%s|%s" % (str(f1), str(f2), str(time_difference)))
# 					fingerprinted.add((i, i + j))
# 	return h



def main(filename):
	fingerprint = location_fingerprint(filename)
	return fingerprint_pair_hashing(fingerprint)

if __name__ == '__main__':	
	main(filename)