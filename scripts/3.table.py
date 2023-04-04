import myutils
import json
lms = ['Twitter/twhin-bert-large', 'Maltehb/aelaectra-danish-electra-small-cased']

treebank = 'UD_English-Tweebank2.UD_Danish-DDT'
for lm in lms:
    lm = lm.replace('/', '_')
    scores = []
    for norm in 'orig', 'norm':
        in_path = 'danish-tiktok-test.conllu-' + norm
        out_path = 'preds/test.' + lm + '.' + in_path + '.eval'
        score = json.load(open(out_path))['UPOS-acc.']
        scores.append(score)
    print(' & '.join([lm] + ['{:.2f}'.format(score*100) for score in scores]))

