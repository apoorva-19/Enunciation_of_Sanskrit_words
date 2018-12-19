if __name__ == '__main__':
    inputfile = input("Enter the file name")
    # scripture = input("Enter the scripture")
    # scripture_acro = input("Enter the scripture acronym")
    scripture = 'Bhagvad Gita'
    scripture_acro = 'BG'
    chapter = int(input("Enter the chapter number"))
    chapter_format = '{:02d}'
    verse_format = '{:03d}'
    openfile = open(inputfile, "r")
    i = 0
    final_shloka = []
    first_line = openfile.readline()

    while first_line:
        first_line.replace("\n", "")
        first_line.strip()
        next_line = openfile.readline()
        next_line.replace("\n", "")
        next_line.strip()
        final_shloka.append(first_line[:-1]+" "+next_line[:-1])
        openfile.readline()
        first_line = openfile.readline()
    
    openfile.close()
    insertfile = open("insert_shloka.txt", "a")
    insert_query = "INSERT INTO shlokas VALUES('{}', '{}', {}, {}, '{}');"
    while i < len(final_shloka):
        shloka_id=scripture_acro+chapter_format.format(chapter)+verse_format.format(i+1)
        insertfile.write(insert_query.format(shloka_id, scripture, chapter, i+1, final_shloka[i])+"\n")
        i += 1

    
