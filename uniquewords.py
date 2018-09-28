from cltk.tokenize.sentence import TokenizeSentence

#initializing tokenizer
tokenizer = TokenizeSentence('sanskrit')

if __name__ == '__main__':
    import sys

if len(sys.argv) == 1:
    print('Needs filename for extracting the unique words from the shlokas')
    sys.exit(-1)

def check_token(token):
    flag = True
    if token == '।':
        flag = False
    elif token.isdigit():
        flag = False

    return flag
    
#building a unique set of words
uniquewords = set()
filestring = []

#extracting words from the text file
unique="unique_words.txt"
uniquefile = open(unique, "r")

string = uniquefile.readline()
while string:
    string = string[:-1]
    uniquewords.add(string)
    string = uniquefile.readline()

uniquefile.close()

#extracting shlokas from the text file
infilename = sys.argv[1]
infile = open(infilename, "r")
string = infile.readline()
while string:
    string = string[:-1]
    #replacing all the '-' with spaces to split into unique words
    string = string.replace('-', ' ')
    filestring.append(string)
    string = infile.readline()

infile.close()

for shlok in filestring:
    #tokenizing each shloka
    tokenized = tokenizer.tokenize(shlok)
    for token in tokenized:
        #checking for the presence of purna-viram, numbers and blank spaces
        if check_token(token) and len(token) > 0:
            uniquewords.add(token)
        
uniquefile = open(unique, "w")

for word in uniquewords:
    uniquefile.write(word+"\n")

uniquefile.close()