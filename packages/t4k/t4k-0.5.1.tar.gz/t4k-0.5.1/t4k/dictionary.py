def invert_dict(dictionary):
	new_dict = {}
	for key in dictionary:
		new_dict[dictionary[key]] = key

	return new_dict


def merge_dicts(*dictionaries):
	merged = {}
	for dictionary in reversed(dictionaries):
		merged.update(dictionary)
	return merged


def dzip(*dictionaries):
	'''
	Like zip, but for dictionaries.  Produce a dictionary whose keys are 
	given by the intersection of input dictionaries' keys, and whose
	values are are tuples of the input dicts corresponding values.
	'''

	# Define the dzip of no dictionaries to be an empty dictionary
	if len(dictionaries) == 0:
		return {}

	# Get the keys common to all dictionaries
	keys = set(dictionaries[1])
	for d in dictionaries[1:]:
			keys &= set(d)

	# Make the zipped dictionary
	return {
		key : tuple([d.get(key, None) for d in dictionaries])
		for key in keys
	}
