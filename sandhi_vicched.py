from cltk.corpus.sanskrit.itrans.unicode_transliterate import ItransTransliterator
from cltk.tokenize.sentence import TokenizeSentence
from cltk.stem.sanskrit.indian_syllabifier import Syllabifier

lang = "hi"
language = "hindi"
tokenizer = TokenizeSentence("sanskrit")
syl = Syllabifier(language)

#List of phonemes that should not be counted as separate diphones while splitting
check_phonemes_1 = ["ः", "ऽ", "ङ्‍\u200d"]
check_phonemes_2 = ["\u200c"]

#List of characters that should be taken to the left in case they are present to the right while splitting
move_left_1 = ['म्','र्','न्']

#Checking for numbers and purna-viram
def check_token(token):
    flag = True
    if token == "।":
        flag = False
    elif token.isdigit():
        flag = False

    return flag

#Checking for splitting position 
def check_proximity(split, pos, next_token):
    if len(split) - pos in range(1, 3):
        if (next_token == "।" or next_token == "॥"):
            return False

    return True

#Checking for the presence of phonemes in check_phonemes_1 and check_phonemes_2
def check_internally(split, pos):
    for ph in check_phonemes_1:
        if split.count(ph) > 0:
            pos += split.count(ph)

    #presence of \u200c means that the word/phrase ends in a half character
    for ph in check_phonemes_2:
        if split.count(ph) > 0:
            pos += 2*split.count(ph)
    return pos

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print("Needs filename for splitting shlokas and for storing split shlokas")
        sys.exit(-1)
    elif len(sys.argv) == 2:
        print("Needs filename for storing split shlokas")
        sys.exit(-1)

    #Accepting user input
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    filestring = []

    infile = open(infilename, "r")

    string = infile.readline()
    while string:
        string = string[:-1]
        filestring.append(string)
        string = infile.readline()

    infile.close()
    outfile = open(outfilename, "w")

    for shlok in filestring:
        
        #picking one shloka from the file
        t_shlok = tokenizer.tokenize(shlok)
        #initializing the flags
        count = 0 # to count the number of phonemes after which the split has to be done
        pos = 0 # to insert the - 
        diff = 0 # to keep track of the overflow phonemes

        for i in range(len(t_shlok)):
            token = t_shlok[i]
            split = syl.orthographic_syllabify(token)
            l = len(split)
            
            # phonemes already covered
            prev = count

            #checking for purna-viram and numbers
            if l == 1 and check_token(token) == False:
                diff = pos = count = 0
                continue

            # more phonemes added
            count = count + l
            
            # word extends the meter length
            if count > 8:                
                # calculates the position for split after checking the internal characters
                pos = check_internally(split[0:8-prev+1], 8-prev)                
                #calculates the overflow phonemes from the current word                
                diff = l - pos

                count = 0

            elif count == 8:
                count = 0
            
            else:
                count = count - check_internally(split, 0)
            while diff > 0:
                if check_proximity(split, pos, t_shlok[i+1]):
                    split.insert(pos, '-')
                    if len(split[pos+1]) > 1:
                        if split[pos+1].count('्') == 1 and split[pos+1][0:2] in move_left_1:
                            #move the half character to the left
                            #here the half character is a combination of the full character and a halant
                            split[pos - 1] = split[pos - 1] + split[pos + 1][0:2]
                            split[pos + 1] = split[pos + 1].replace(split[pos + 1][0:2], "")
                            #when it is split again the half character will be counted separately
                            pos += 1
                        
                        elif split[pos+1].count('्') > 1:
                            #more than one half characters are present here
                            #move the first half character to the left irrespective of the character being in the move_left list or not
                            #here the half character is a combination of the full character and a halant
                            split[pos - 1] = split[pos - 1] + split[pos + 1][0:2]
                            split[pos + 1] = split[pos + 1].replace(split[pos + 1][0:2], "")
                            #when it is split again the half character will be counted separately
                            pos += 1
                    #pos is incremented to account for the dash that has been added
                    pos += 1
                # joining a word
                token = "".join(map(str, split))
                # split it again to break the word again
                split = syl.orthographic_syllabify(token)
                if diff < 8:
                    count = diff
                    pos = diff = 0
                    t_shlok[i] = "".join(map(str, split))
                elif diff > 8:
                    diff = diff - 8
                    pos = pos + 8
                else:
                    diff = 0
                    t_shlok[i] = "".join(map(str, split))
                # print (split)
                # print ("diff: {}, count: {}, pos:{}".format(diff, count, pos))

            # joining the words together to form the shloka
        broken = " ".join(map(str, t_shlok))
        outfile.write(broken + "\n")

    outfile.close()      