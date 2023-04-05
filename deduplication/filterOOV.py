danish_words = set([word.strip() for word in open('aspell-da.txt')])
danish_words.add('@username')

outFile = open('allcomments-filterOOV.txt', 'w')
for line in open('allcomments.txt'):
    tok = line.strip().lower().split(' ')
    oovs = 0
    total = 0

    for token in tok:
        has_alpha = False
        for char in token:
            if char.isalpha():
                has_alpha = True
        if token not in danish_words and has_alpha:
            oovs += 1
        if has_alpha and token != '@username':
            total += 1
    if total == 0:
        continue
    ratio = oovs/total
    if ratio > .1 and ratio < .6:
        outFile.write(line)
    #    print(line.strip(), ratio)
    else:
        print(line.strip(), ratio)
outFile.close()

