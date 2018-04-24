import sys
import os

myletters = {1:u'\u0c85',
2:u'\u0c86',
3:u'\u0c87',
4:u'\u0c88',
5:u'\u0c89',
6:u'\u0c8a',
7:u'\u0c8b',
8:u'\u0ce0',
9:u'\u0c8e',
10:u'\u0c8f',
11:u'\u0c90',
12:u'\u0c92',
13:u'\u0c93',
14:u'\u0c94',
15:u'\u0c85\u0c82',
16:u'\u0c85\u0c83',
17:u'\u0c95',
18:u'\u0c96',
19:u'\u0c97',
20:u'\u0c98',
21:u'\u0c99',
22:u'\u0c9a',
23:u'\u0c9b',
24:u'\u0c9c',
25:u'\u0c9d',
26:u'\u0c9e',
27:u'\u0c9f',
28:u'\u0ca0',
29:u'\u0ca1',
30:u'\u0ca2',
31:u'\u0ca3',
32:u'\u0ca4',
33:u'\u0ca5',
34:u'\u0ca6',
35:u'\u0ca7',
36:u'\u0ca8',
37:u'\u0caa',
38:u'\u0cab',
39:u'\u0cac',
40:u'\u0cad',
41:u'\u0cae',
42:u'\u0caf',
43:u'\u0cb0',
44:u'\u0cb2',
45:u'\u0cb5',
46:u'\u0cb6',
47:u'\u0cb7',
48:u'\u0cb8',
49:u'\u0cb9',
50:u'\u0cb3',
51:u'\u0cde',
52:u'\u0cb1'}

mynumbers = {0:u'\u0ce6',
1:u'\u0ce7',
2:u'\u0ce8',
3:u'\u0ce9',
4:u'\u0cea',
5:u'\u0ceb',
6:u'\u0cec',
7:u'\u0ced',
8:u'\u0cee',
9:u'\u0cef'}

"""
	ra can appear as ottakshara in 2 forms (Analyse the pronounciation of below words)
		1. Krama - Use normal method as used for rest of the consonant clusters formation (Try : 17^43C41)
		2. Karma - Use below method (Try: 17C41+17)

	myvowels[17]:u'\u0cb0'

	Needed for special case 1 of "Ra"

	ra + halant + ka 
	
	Expected - ra is main character and ka is ottakshara
	Actual output - ka is main character, ra is ottakshara(example - Karma)

"""

myvowels = {
1:u'\u0ccd',
2:u'\u0cbe',
3:u'\u0cbf',
4:u'\u0cc0',
5:u'\u0cc1',
6:u'\u0cc2',
7:u'\u0cc3',
8:u'\u0cc4',
9:u'\u0cc6',
10:u'\u0cc7',
11:u'\u0cc8',
12:u'\u0cca',
13:u'\u0ccb',
14:u'\u0ccc',
15:u'\u0c82',
16:u'\u0c83',
17:u'\u0cb0'}

"""
    zwj 
    Needed for special case 2 of "Ra" 

    ra + zwj + halant + ottakshara(consider na)

    (Try: 43^36)

    where ra is to be treated as main character and not ottakshara

"""

myspecials = {
1:u'\u200d'  
}

def decode_word(word):
	myword = ""
	# Split each word into characters with ottaksharas and kagunitas(vowels)
	chars = word.split('C')
	for i in range(0, len(chars)):
		# Keep track of vowels 
		vowelflag = False
		vowel=""
		cons=""
		if('+' in chars[i]):
			""" 
				Vowels exist. Extract vowel and use rest to split into consonant and ottaksharas.
				
				A character with ottaksharas and vowels are always formed in unicode by following method

					main_character + ottakshara_1 + ottakshara_2 +...ottakshara_n + vowel
				
				Note: There can be any number of ottaksharas for a main_character but only one vowel

			"""
			vowel = chars[i].split('+')[1]
			vowelflag = True
			cons = chars[i].split('+')[0]
			cons = cons.split('^')
		else:
			cons = chars[i].split('+')[0]
			cons = chars[i].split('^')
		# Start forming character with ottaksharas and vowels to print
		mychar = ""
		for j in range(0,len(cons)):
			mychar += myletters[int(cons[j])]
			""" 
				If ra appears as a consonant, we need to preserve it so that it doesnt become a ottakshara.
				This is special case 2 that was discussed above.
			"""
			if(int(cons[j]) == 43):
				mychar += myspecials[1]
			"""
				We are at character level, first character is main character, rest are all ottaksharas. 
				So add halant characters in order to form consonant clusters
			"""        
			if(j!=len(cons)-1):
				if(vowelflag==False):
					mychar += myvowels[1]
				else:
					# In order to handle special case 1 of ra. Do not add halant to main character if vowel is 17
					if(int(vowel)!=17):
						mychar += myvowels[1]
		if(vowelflag):
			"""
				If vowel is 17, as mentioned before, we have not added halant to main character
				To obtain required output, we use special case 1 formula

									ra + halant + ka 

			"""
			if(int(vowel) == 17):    
				newchar = myvowels[int(vowel)]
				newchar = newchar + myvowels[1] 
				newchar += mychar
				mychar = newchar
			# Else use normal method to concatenate consonant with vowels
			else:
				mychar += myvowels[int(vowel)]
		print(mychar)
		# Once char is obtained, form words
		myword += mychar
	# Spaces between words
	myword +=" "
	print(myword)
	return(myword)

"""
	Input form
		L - Seperate lines
		W - Seperate words
		C - Seperate characters
		^ - Seperate ottaksharas in characters
		+ - Seperate vowel
"""

# Input - "36C36^36W49+9C48C43+5W46^43+10C42+2L36+3C36^36W49+9C48C43+5W46+5C40^43C24^42+13C32+3"
input = sys.argv[1]
lines = input.split('L')
line_count = 0
word_count = 0
for i in range(0,len(lines)):
	myline = ""
	print(lines[i])
	line_count += 1
	words = lines[i].split('W')
	for j in range(0, len(words)):
		print(words[j])
		myword = decode_word(words[j])
		myline = myline + myword
	print(myline)