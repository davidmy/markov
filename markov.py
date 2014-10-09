from random import random
import sys

markov = {}
prefix_length = 5
max_sentence_length = 1024
num_output = 1

def get_dist(prefix):
	'''Return the dictionary associated with the key 'prefix'.'''
	
	global markov
	if prefix in markov:
		# return existing symbol distribution
		return markov[prefix]
	else:
		# create new distribution and return it
		dist = {}
		markov[prefix] = dist
		return dist

def add_symbol(dist, word):
	'''Adds a number to a key in a dictionary.'''
	
	if word in dist:
		dist[word] = dist[word] + 1
	else:
		dist[word] = 1

def pick_symbol(dist):
	'''Picks a random key from a dictionary, with a probability of the
	value/sum(values)'''
	
	# pick a random number n, such that 0 <= n < sum(values in distribution)
	pick = int(sum([dist[key] for key in dist])*random())
	
	# sum up the values until we reach the number we picked
	s = 0
	for key in dist:
		s = s + dist[key]
		if pick < s:
			return key
	return '$'
	
def learn(data):
	'''Train data into the markov chain.'''
	
	global prefix_length
	prefix = '^'
	data = data + '$'
	for c in data:
		if c == '\n': continue
		add_symbol(get_dist(prefix), c)
		prefix = prefix + c
		prefix = prefix[-prefix_length:]

def generate():
	'''Generate a random markov chain.'''
	
	global max_sentence_length, prefix_length
	c = '^'
	s = ''
	prefix = ''
	while len(s) < max_sentence_length:
		prefix = prefix + c
		prefix = prefix[-prefix_length:]
		c = pick_symbol(get_dist(prefix))
		if c == '$':
			break
		else:
			s += c
	return s

def main():
	global prefix_length, num_output, markov
	
	i = 1
	help = False
	show_stats = False
	while i < len(sys.argv):
		arg = sys.argv[i]
		i = i + 1
		if arg == '-n':
			num_output = int(sys.argv[i])
			i = i + 1
		elif arg == '-p':
			prefix_length = int(sys.argv[i])
			i = i + 1
		elif arg == '--stats':
			show_stats = True
		else: help = True

	if help:
		print \
'''Usage: python markov.py [-p PREFIX_LENGTH] [-n NUM_OUTPUTS]
Generates a markov chain based on standard input.

Options:
  -p PREFIX_LENGTH  Sets the length of the prefix used in the learning
                      algorithm.
  -n NUM_OUTPUTS    Sets the number of outputs.
  
Example:
	cat story1.txt story2.txt | python markov.py -p 5 -n 10
'''
	else:
		for line in sys.stdin:
			learn(line)
	
		if show_stats:
			print 'Number of prefixes:', len(markov)
			print 'Max num of postfixes:', max([len(markov[key]) for key in markov])
			print 'Avg num of postfixes:', float(sum([len(markov[key]) for key in markov]))/len(markov)
			pass
		else:
			for i in range(num_output):
				print generate()

main()
