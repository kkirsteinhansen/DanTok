import json
import myutils

outDir = 'preds/'


mlm_id = {'vinai/bertweet-base', 'vinai/bertweet-large', 'cardiffnlp/twitter-xlm-roberta-base', 'cardiffnlp/twitter-roberta-base', 'jhu-clsp/bernice', 'Twitter/twhin-bert-large'}
mlm_il = {'Maltehb/danish-bert-botxo', 'jhu-clsp/bernice', 'Twitter/twhin-bert-large', 'cardiffnlp/twitter-xlm-roberta-base', 'DDSC/roberta-base-danish', 'Maltehb/aelaectra-danish-electra-small-cased'}
data_id = {'UD_English-Tweebank2'}
data_il = {'UD_Danish-DDT'}
devPath = 'danish-tiktok-dev.conllu'

def conv(boolean):
    if boolean:
        return '+'
    else:
        return '-'
        
all_trains = myutils.trains + ['UD_English-Tweebank2.UD_Danish-DDT']
treebank_names = []
for treebank  in all_trains:
    if '.' in treebank:
        short_name = 'tweebank+DDT'
    else:
        train, dev, test = myutils.getTrainDevTest('machamp/data/ud-treebanks-v2.11.singleToken/' + treebank)
        short_name = train.split('/')[-1].split('-')[0].replace('_', '\\_')
    if short_name == 'en':
        short_name = 'en\\_tweebank'
    treebank_names.append(short_name)


for norm in 'orig', 'norm':
    print(norm)
    print(' & '.join([''] + treebank_names) + ' \\\\')
    for mlm in myutils.mlms:
        scores = []
        for treebank in all_trains:
            mlm_name = mlm.replace('/', '_')
            name = treebank + '.' + mlm_name
        
            outPath = outDir + '/' + name + '.' + devPath + '-' + norm + '.eval'
            score = json.load(open(outPath))['UPOS-acc.']
            scores.append('{:.2f}'.format(score*100))
        print(' & '.join([mlm.split('/')[-1]] + scores) + ' \\\\')

