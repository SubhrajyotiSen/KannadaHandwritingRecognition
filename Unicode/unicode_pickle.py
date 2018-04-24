import pickle as pkl

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
52:u'\u0cb1',
53:u'\u0cb0'}

"""
	SPECIAL CASE 1 OF Ra

	53rd letter explanation - 

	ra can appear as ottakshara in 2 forms (Analyse the pronounciation of below words)
		1. Krama - Use normal method as used for rest of the consonant clusters formation (Try : 17^43C41)
		2. Karma - Use below method (Try: 17C41+17)

	myletters[53]:u'\u0cb0'

	Needed for special case 1 of "Ra"

	ra + halant + ka 
	
	Expected - ra is main character and ka is ottakshara
	Actual output - ka is main character, ra is ottakshara(example - Karma)

"""

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
}

"""
	SPECIAL CASE 2 OF Ra
	
    zwj 
    Needed for special case 2 of "Ra" 

    ra + zwj + halant + ottakshara(consider na)

    (Try: 43^36)

    where ra is to be treated as main character and not ottakshara

"""

myspecials = {
1:u'\u200d'  
}

# create a list of the dictonaries
dictionaries = [myletters, mynumbers, myvowels, myspecials]

# store the list of dictionaries as a single pickle file
pkl.dump( dictionaries, open("kannada_unicode.p", "wb"))