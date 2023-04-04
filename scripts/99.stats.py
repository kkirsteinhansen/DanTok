import myutils

def conv(score):
    return '{:.2f}'.format(score)

for lm in myutils.mlms:
    match = 'UD_English-Tweebank2.' + lm.replace('/', '_') + '.danish-tiktok-dev.conllu-orig'
    on = False
    unks = None
    subwords = None
    words = None
    for line in open('scripts/1.pred.out'):
        if match in line: 
            on = True
        if on == True and 'Unks' in line and unks == None:
            unks = int(line.strip().split(' ')[-1].replace(',', ''))
        if on == True and 'Words' in line and words == None:
            words = int(line.strip().split(' ')[-1].replace(',', ''))
        if on == True and 'Subwords' in line and subwords == None:
            subwords = int(line.strip().split(' ')[-1].replace(',', ''))
    print(lm, conv(unks/words), conv(subwords/words))
