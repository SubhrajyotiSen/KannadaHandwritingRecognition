
myletters = {
    0: u'\u0c85',
    1: u'\u0c86',
    2: u'\u0c87',
    3: u'\u0c88',
    4: u'\u0c89',
    5: u'\u0c8a',
    6: u'\u0c8b',
    7: u'\u0c8e',
    8: u'\u0c8f',
    9: u'\u0c90',
    10: u'\u0c92',
    11: u'\u0c93',
    12: u'\u0c94',
    13: u'\u0c85\u0c82',
    14: u'\u0c85\u0c83',
    16: u'\u0c95',
    17: u'\u0c96',
    18: u'\u0c97',
    19: u'\u0c98',
    20: u'\u0c99',
    21: u'\u0c9a',
    22: u'\u0c9b',
    23: u'\u0c9c',
    24: u'\u0c9d',
    25: u'\u0c9e',
    26: u'\u0c9f',
    27: u'\u0ca0',
    28: u'\u0ca1',
    29: u'\u0ca2',
    30: u'\u0ca3',
    31: u'\u0ca4',
    32: u'\u0ca5',
    33: u'\u0ca6',
    34: u'\u0ca7',
    35: u'\u0ca8',
    36: u'\u0caa',
    37: u'\u0cab',
    38: u'\u0cac',
    39: u'\u0cad',
    40: u'\u0cae',
    41: u'\u0caf',
    42: u'\u0cb0',
    43: u'\u0cb2',
    44: u'\u0cb5',
    45: u'\u0cb6',
    46: u'\u0cb7',
    47: u'\u0cb8',
    48: u'\u0cb9',
    49: u'\u0cb3',
    50: u'\u0cb0',
    51: u'\u0c83'}

"""
	SPECIAL CASE 1 OF Ra

	50th letter explanation - 

	ra can appear as ottakshara in 2 forms (Analyse the pronounciation of below words)
		1. Krama - Use normal method as used for rest of the consonant clusters formation (Try : 17^43C41)
		2. Karma - Use below method (Try: 17C41+17)

	myletters[50]:u'\u0cb0'

	Needed for special case 1 of "Ra"

	ra + halant + ka 
	
	Expected - ra is main character and ka is ottakshara
	Actual output - ka is main character, ra is ottakshara(example - Karma)

"""

mynumbers = {0: u'\u0ce6',
             1: u'\u0ce7',
             2: u'\u0ce8',
             3: u'\u0ce9',
             4: u'\u0cea',
             5: u'\u0ceb',
             6: u'\u0cec',
             7: u'\u0ced',
             8: u'\u0cee',
             9: u'\u0cef'}

myvowels = {
    0: u'\u0ccd',
    1: u'\u0cbe',
    2: u'\u0cbf',
    3: u'\u0cc0',
    4: u'\u0cc1',
    5: u'\u0cc2',
    6: u'\u0cc3',
    7: u'\u0cc6',
    8: u'\u0cc7',
    9: u'\u0cc8',
    10: u'\u0cca',
    11: u'\u0ccb',
    12: u'\u0ccc',
    13: u'\u0c82',
    14: u'\u0c83',
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
    1: u'\u200d'
}


def get_dictionaries():
    return myletters, mynumbers, myvowels, myspecials
