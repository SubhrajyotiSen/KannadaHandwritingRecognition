import Unicode.unicode_dict as ud

# load the unicode dictionaries
myletters, mynumbers, myvowels, myspecials = ud.get_dictionaries()


def decode_word(word):
    myword = ""
    # Split each word into characters with ottaksharas and kagunitas(vowels)
    chars = word.split('C')
    for i in range(1, len(chars)):
        # Keep track of vowels
        vowelflag = False
        vowel = ""
        cons = ""
        numbers = ""
        # Split the word based on N and get invidual digits
        if(chars[i][0] == 'N'):
            # Append the digits to form higher numbers
            myword += mynumbers[int(chars[i][1])]
        else:
            if('+' in chars[i]):
                """ 
                        Vowels exist. Extract vowel and use rest to split into consonant and ottaksharas.

                        A character with ottaksharas and vowels are always formed in unicode by following method

                                main_character + ottakshara_1 + ottakshara_2 +...ottakshara_n + vowel

                        NOTE: There can be any number of ottaksharas for a main_character but only one vowel

                """
                vowel = chars[i].split('+')[1]
                vowelflag = True
            cons = chars[i].split('+')[0].split('^')

            # Start forming character with ottaksharas and vowels to print
            mychar = ""
            for j in range(0, len(cons)):
                # If cons[j] is 50, it is handled in previous iteration. So skip and continue.
                if(int(cons[j]) == 50):
                    continue

                mychar += myletters[int(cons[j])]

                """ 
					If ra appears as a main consonant(that is j = 0), we need to preserve it so that it doesnt become a ottakshara.
					This is special case 2 that was discussed above.
				"""
                if(int(cons[j]) == 42 and j == 0):
                    mychar += myspecials[1]
                """
					We are at character level, first character is main character, rest are all ottaksharas. 
					So add halant characters in order to form consonant clusters
				"""
                added = False  # Bad way of handling this. Change it
                if(j != len(cons)-1):
                    # Check if next ottakshara to add is 53. If yes, this has to be handled as per special case 1 of ra
                    if(j+1 != len(cons)):
                        if(int(cons[j+1]) == 50):
                            newchar = myletters[42]
                            newchar = newchar + myvowels[0]
                            newchar += mychar
                            mychar = newchar
                            added = True
                    # Add ottakshara normally
                if(j != len(cons)-1 and added is False):
                    mychar += myvowels[0]

            # Check if vowels exist and add them
            if(vowelflag):
                mychar += myvowels[int(vowel)]
                if(int(vowel) == 0):
                    mychar += myspecials[1]
            # Once char is obtained, form words
            myword += mychar
    # Spaces between words
    myword += " "
    return(myword)


"""
	Input form
		L - Seperate lines
		W - Seperate words
		C - Seperate characters
		N - Separate numbers
		^ - Seperate ottaksharas in characters
		+ - Seperate vowel
"""


def unicode_to_kn(input):
    mydoc = []
    lines = input.split('L')
    for i in range(1, len(lines)):
        myline = ""
        # print(lines[i])
        words = lines[i].split('W')
        for j in range(1, len(words)):
            myword = decode_word(words[j])
            myline = myline + myword
        mydoc.append(myline)
    return mydoc
