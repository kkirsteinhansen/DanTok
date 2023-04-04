import os
import myutils

dev_path = 'danish-tiktok-dev.conllu'
outDir = 'preds/'
if not os.path.isdir(outDir):
    os.mkdir(outDir)

for treebank in myutils.trains:
    for mlm in myutils.mlms:
        mlm_name = mlm.replace('/', '_')
        name = treebank + '.' + mlm_name
        model_path = myutils.getModel(name) 
        if model_path != '':
            for norm in True, False:
                inPath = dev_path
                if norm:
                    inPath += '-norm' 
                else:
                    inPath += '-orig' 
                outPath = outDir + '/' + name + '.' + inPath
                cmd = 'python3 predict.py ' + model_path.replace('machamp/', '') + ' ../' + inPath + ' ../' + outPath
                #if not os.path.isfile(outPath):
                print(cmd)


for mlm in myutils.mlms:
    mlm_name = mlm.replace('/', '_')
    name = '.'.join(myutils.trains[1:]) + '.' + mlm_name
    model_path = myutils.getModel(name) 
    if model_path != '':
        for norm in True, False:
            inPath = dev_path
            if norm:
                inPath += '-norm'
            else:
                inPath += '-orig'
            outPath = outDir + '/' + name + '.' + inPath
            cmd = 'python3 predict.py ' + model_path.replace('machamp/', '') + ' ../' + inPath + ' ../' + outPath + ' --dataset ' + myutils.trains[1]
            #if not os.path.isfile(outPath):
            print(cmd)

