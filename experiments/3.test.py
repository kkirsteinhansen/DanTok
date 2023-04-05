import myutils

lms = ['Twitter/twhin-bert-large', 'Maltehb/aelaectra-danish-electra-small-cased']

treebank = 'UD_English-Tweebank2.UD_Danish-DDT'
for lm in lms:
    lm = lm.replace('/', '_')
    for norm in 'norm', 'orig':
        model_name = treebank + '.' + lm
        model_path = myutils.getModel(model_name)
        in_path = 'danish-tiktok-test.conllu-' + norm
        out_path = 'preds/test.' + lm + '.' + in_path 
        print('python3 predict.py ' + model_path.replace('machamp/', '') + ' ../' + in_path + ' ../' + out_path  + ' --dataset ' + myutils.trains[1])
        
