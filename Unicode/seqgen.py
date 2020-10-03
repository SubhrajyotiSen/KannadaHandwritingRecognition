import Unicode.seqdictionary as sd

"""
	The input to the script is a dictionary of key value pair as mentioned below 
	filename : class number

	filename is of string format = LL-WW-CC-O
	(where O is 0 if it is not ottakshara and is 1,2...n if ottakshara)
	
"""

kagunita_mapping = sd.get_dictionaries()


def is_a(char):
    aa = [0]
    if(char in aa):
        return True


def is_vowel(char):
    vowels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    if(char in vowels):
        return True


def is_number(char):
    numbers = [559, 560, 561, 562, 563, 564, 565, 566, 567, 568]
    if(char in numbers):
        return True


def addottakshara(myseq, ott):
    if(ott == 6):
        myseq = myseq + "+" + "6"
    elif(ott == 9):
        initial_vowel = int(myseq.rsplit('+')[-1])
        vowel_len = len(str(initial_vowel))
        print(vowel_len)
        myseq = myseq[0: len(myseq)-vowel_len]
        myseq = myseq + "9"
    elif('+' in myseq):
        letter = myseq.split('+')[0]
        vowel = myseq.split('+')[1]
        myseq = letter + "^" + str(ott)
        myseq = myseq + "+" + vowel
    else:
        myseq = myseq + "^" + str(ott)
    return myseq


def addchar(seq, chars, otts, prevchar):
    """
            Handle dhirga 
            In case 3,8 and 11 vowel when added to a consonant forming kagunita is split during character segmentation

            If 569 is encountered, access the vowel added to last letter in the sequence.
            Add 1 to it so that 2,7 and 10 become 3,8 and 11 respectively

            Obtain substring excluding the last vowel, and add the new vowel to it.

    """
    previous_vowel = is_vowel(prevchar)
    previous_number = is_number(prevchar)
    previous_a = is_a(prevchar)
    if(chars == 569):
        if(not previous_vowel and not previous_number and not previous_a):
            last_added = seq.rsplit('C')[-1]
            if('+' in last_added):
                initial_vowel = last_added.rsplit('+')[-1]
                print("initial_vowel", initial_vowel)
                if(initial_vowel.isdigit()):
                    initial_vowel = int(initial_vowel)
                    vowel_len = len(str(initial_vowel))
                    seq = seq[0: len(seq)-vowel_len]
                    if(initial_vowel == 2 or initial_vowel == 7 or initial_vowel == 10):
                        seq = seq + str(initial_vowel+1)
                    else:
                        arr = [3, 8, 11]
                        close = min(arr, key=lambda x: abs(x-initial_vowel))
                        seq = seq + str(close)
            else:
                seq = seq + "+3"
        return seq

    """
		570 is matra of vowel 14.
		If encountered as a character, add it to the immediate previous letter in the sequence
	"""
    if(chars == 570):
        if(not previous_vowel and not previous_number):
            seq = seq + "C" + kagunita_mapping[570]
        return seq

    """
		559 class is considered as number 0 if
			1. It occurs at the beginning of a new word (LWCN0)
			2. It occurs in the middle of a word which is made up of numbers (LWCN9CN4CN0)

		Else, that is if 559 occurs in between a word made up of letters, it is considered as vowel 13 matra 
		and is added to immediate previous letter in the sequence
	"""
    if(chars == 559):
        if(not previous_vowel):
            seq = seq + "C" + kagunita_mapping[559]
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
        print("last", last_added)
        if(last_added and 'N' not in last_added and 'C' not in last_added):
            seq = seq + ""
        if(last_added and 'N' not in last_added and not previous_vowel):
            if('+' in last_added):
                letter = last_added.split('+')[0]
                vowel = last_added.split('+')[1]
                seq = seq[0:len(seq)-len(last_added)]
                seq = seq + letter + "^" + "50"
                seq = seq + "+" + vowel
                print("Seq", seq)
            else:
                seq = seq + "^" + "50"
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
        if(ott != "" and not is_vowel(chars) and not is_number(chars)):
            myseq = addottakshara(myseq, ott)

    return seq + myseq


def sequenceGen(input):
    sequence = ""
    # Obtain all keys
    keys = input.keys()
    # Sort all keys. Just to be sure they are in order of line, word and characters if they werent already
    sorted_input = sorted(keys)
    # print(sorted_input)
    i = 0
    # Select first entry and check its line number.
    while(i < len(sorted_input)):
        # print(len(sorted_input))
        line = sorted_input[i][:2]
        # print("i:", i, "line: ", line)
        sequence = sequence + "L"
        j = i
        # Access all words present in line i that is in consideration
        while(j < len(sorted_input) and sorted_input[j][:2] == line):
            word = sorted_input[j][3:5]
            sequence = sequence + "W"
            k = j
            # print("j:", j, "word: ", word)
            # Access all characters present in word j that is in consideration
            while(k < len(sorted_input) and sorted_input[k][3:5] == word and sorted_input[k][:2] == line):
                # Send each character along with its associated ottaksharas to append it to the sequence
                mychars = input[sorted_input[k]]
                myotts = []
                # print("k:", k, "char: ", mychars)
                for o in range(k+1, len(sorted_input)+1):
                    if(o == len(sorted_input)):
                        break
                    char = sorted_input[o][9]
                    if(int(char) != 0):
                        myotts.append(input[sorted_input[o]])
                        # print("o:", o, "otts ", myotts)
                    else:
                        break
                # print("mychars: ", mychars,"myotts: ",myotts)
                sequence = addchar(sequence, mychars, myotts,
                                   input[sorted_input[k-1]])
                # print(sequence)
                k = o
                #print("k:", k, ",o:", o)
            j = k
            #print("j:", j, ",k:", k)
        i = j
        #print("i:", i, ",j:", j)
    return(sequence)
