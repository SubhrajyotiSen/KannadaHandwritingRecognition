import sys
import os
import seqdictionary as sd

"""
	The input to the script is a dictionary of key value pair as mentioned below 
	filename : class number

	filename is of string format = LL-WW-CC-O
	(where O is 0 if it is not ottakshara and is 1,2...n if ottakshara)
	
"""


kagunita_mapping = sd.get_dictionaries()

def addchar(seq, chars, otts):

	"""
		Handle dhirga 
		In case 3,8 and 11 vowel when added to a consonant forming kagunita is split during character segmentation

		If 569 is encountered, access the vowel added to last letter in the sequence.
		Add 1 to it so that 2,7 and 10 become 3,8 and 11 respectively

		Obtain substring excluding the last vowel, and add the new vowel to it.

	"""
	if(chars == 569):
		initial_vowel = int(seq.rsplit('+')[-1])
		vowel_len = len(str(initial_vowel))
		seq = seq[0: len(seq)-vowel_len]
		seq = seq + str(initial_vowel+1)
		print(seq)
		return seq

	"""
		570 is matra of vowel 14.
		If encountered as a character, add it to the immediate previous letter in the sequence
	"""
	if(chars == 570):
		seq = seq + "+" + kagunita_mapping[14]
		return seq

	"""
		559 class is considered as number 0 if
			1. It occurs at the beginning of a new word (LWCN0)
			2. It occurs in the middle of a word which is made up of numbers (LWCN9CN4CN0)

		Else, that is if 559 occurs in between a word made up of letters, it is considered as vowel 13 matra 
		and is added to immediate previous letter in the sequence
	"""
	if(chars == 559):
		last_added = seq.rsplit('W')[-1]
		print(last_added)
		if(last_added and 'N' not in last_added and 'C' not in last_added):
			seq = seq + ""
		if(last_added and 'N' not in last_added):
			seq = seq + "+" + kagunita_mapping[13]
			return seq

	"""
		568 class is considered as number 9 if
			1. It occurs at the beginning of a new word (LWCN9)
			2. It occurs in the middle of a word which is made up of numbers (LWCN4CN9CN0)

		Else, that is if 568 occurs in between a word made up of letters, it is considered as ra ottakshara 
		and is added to (present-2)th letter in the sequence
	"""
	if(chars == 568):
		last_added = seq.rsplit('W')[-1]
		print("last",last_added)
		if(last_added and 'N' not in last_added and 'C' not in last_added):
			seq = seq + ""
		if(last_added and 'N' not in last_added):
			if('+' in last_added):
				letter = last_added.split('+')[0]
				vowel = last_added.split('+')[1]
				seq = seq[0:len(seq)-len(last_added)]
				seq = seq + letter  + "^" + "50"
				seq = seq + "+" + vowel
				print("Seq", seq)
			else:
				seq = seq  + "^" + "50"
			return seq


	"""
		If it is none of the above cases, then the character obtained is a letter, kagunita or a number.
		In case of letter and number, we can get kagunita_mapping and add it to sequecne

		In case we have got a kagunita, as the mapping returns letter and vowel added to it(Letter+vowel), we need to split it.
		This split is required if there are ottaksharas present for given character as we know that unicode accepts input in the
		following format

				letter + ottakshara1 + ottakshara2 + ..... + vowel

		We split, add ottaksharas and then add back the vowel to get
		(Letter + ottaksharas + vowel)

	"""
	myseq = "C" + kagunita_mapping[chars]
	for ott in otts:
		if(ott == 6):
			myseq = myseq + "+" + "6"
			""" 
				Why? It is vowel. The previous character would have been recognised as normal letter in this case.
				Hence directly add the vowel
			"""
		elif(ott == 9):
			initial_vowel = int(myseq.rsplit('+')[-1])
			vowel_len = len(str(initial_vowel))
			print(vowel_len)
			myseq = myseq[0: len(myseq)-vowel_len]
			myseq = myseq + "9"
			"""
				Why? It is vowel. But as this vowel not only adds the matra at bottom but also has upper section of the letter modified, 
				it would be intially recognised as (letter + vowel 7). Hence remove it and add vowel 9 
			"""
			
		elif('+' in myseq):
			letter = myseq.split('+')[0]
			vowel = myseq.split('+')[1]
			myseq = letter  + "^" + str(ott)
			myseq = myseq + "+" + vowel
		else:
			myseq = myseq  + "^" + str(ott)
	return seq + myseq


def sequenceGen(input):
	sequence = ""
	# Obtain all keys
	keys = input.keys()
	# Sort all keys. Just to be sure they are in order of line, word and characters if they werent already
	sorted_input = sorted(keys)
	print(sorted_input)
	i = 0
	# Select first entry and check its line number. 
	while(i < len(sorted_input)-1):
		line = sorted_input[i][:2]
		sequence = sequence + "L"
		j = i
		# Access all words present in line i that is in consideration
		while(j < len(sorted_input)-1):
			if(sorted_input[j][:2] == line):
				word = sorted_input[j][3:5]
				sequence = sequence + "W"
				k = j
				# Access all characters present in word j that is in consideration
				while(k < len(sorted_input)-1):
					if(sorted_input[k][3:5] == word):
						# Send each character along with its associated ottaksharas to append it to the sequence
						mychars = input[sorted_input[k]]
						myotts = []
						for o in range(k+1, len(sorted_input)):
							char = sorted_input[o][9]
							if(int(char)!=0):
								myotts.append(input[sorted_input[o]])
							else:
								break
						print("mychars: ", mychars,"myotts: ",myotts)
						sequence = addchar(sequence,mychars,myotts)
						print(sequence)
						k = o
					else:
						break		
				j = k
			else:
				break
		i = j
	return(sequence)