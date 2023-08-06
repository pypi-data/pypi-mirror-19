
class Max(object):

	def __init__(self, keep_last=True):
		self.extreme_key = None
		self.extreme_item = None
		self.keep_last = keep_last

	def add(self, key, item):
		if (
			self.extreme_key is None 
			or self.comp(key, self.extreme_key)
			or (self.keep_last and key == self.extreme_key)
		):
			self.extreme_key = key
			self.extreme_item = item

	def update(self, key_item_pairs):
		for key, item in key_item_pairs:
			self.add(key, item)

	def get(self):
		return self.extreme_key, self.extreme_item

	def comp(self, key1, key2):
		return key1 > key2


class Min(object):
	def comp(self, key1, key2):
		return key1 < key2
