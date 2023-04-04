import myutils

devPaths = []
for treebank in myutils.trains:
    train, dev, test = myutils.getTrainDevTest('machamp/data/ud-treebanks-v2.11.singleToken/' + treebank)
    devPaths.append(dev)

devPaths.append('danish-tiktok-dev.conllu-orig')

# open, closed class and Other (https://universaldependencies.org/u/pos/index.html) 
pos_tags = ['ADJ', 'ADV', 'INTJ', 'NOUN', 'PROPN', 'VERB', 'ADP', 'AUX', 'CCONJ', 'DET', 'NUM', 'PART', 'PRON', 'SCONJ', 'PUNCT', 'SYM', 'X']

data = []
for path in devPaths:
    counts = [0] * len(pos_tags)
    for line in open(path):
        if len(line) > 2 and line[0] != '#':
            tok = line.strip().split('\t')
            posIdx = pos_tags.index(tok[3])
            counts[posIdx] += 1
    probs = [count/sum(counts) for count in counts]
    data.append(probs)


myutils.graph(data, pos_tags, myutils.trains + ['DanTok'], 'Frequency (%)', 'distribution.pdf')

