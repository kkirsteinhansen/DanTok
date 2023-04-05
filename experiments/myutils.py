import os
import _jsonnet
import json


mlms = ['Maltehb/danish-bert-botxo', 'DDSC/roberta-base-danish', 'Maltehb/aelaectra-danish-electra-small-cased', 'vinai/bertweet-base', 'vinai/bertweet-large', 'cardiffnlp/twitter-roberta-base', 'cardiffnlp/twitter-xlm-roberta-base', 'jhu-clsp/bernice', 'Twitter/twhin-bert-large']
trains = ['UD_English-LinES', 'UD_English-Tweebank2', 'UD_Danish-DDT']
seeds = ['1']

def getTrainDevTest(path):
    train = ''
    dev = ''
    test = ''
    for conlFile in os.listdir(path):
        if conlFile.endswith('conllu'):
            if 'train' in conlFile:
                train = path + '/' + conlFile
            if 'dev' in conlFile:
                dev = path + '/' + conlFile
            if 'test' in conlFile:
                test = path + '/' + conlFile
    return train, dev, test

def hasColumn(path, idx, threshold=.1):
    total = 0
    noWord = 0
    for line in open(path).readlines()[:5000]:
        if line[0] == '#' or len(line) < 2:
            continue
        tok = line.strip().split('\t')
        if tok[idx] == '_':
            noWord += 1
        total += 1
    return noWord/total < threshold

def getModel(name):
    modelDir = 'machamp/logs/'
    nameDir = modelDir + name + '/'
    if os.path.isdir(nameDir):
        for modelDir in reversed(os.listdir(nameDir)):
            modelPath = nameDir + modelDir + '/model.pt'
            if os.path.isfile(modelPath):
                return modelPath
    return ''

def load_json(path: str):
    """
    Loads a jsonnet file through the json package and returns a dict.
    
    Parameters
    ----------
    path: str
        the path to the json(net) file to load
    """
    return json.loads(_jsonnet.evaluate_snippet("", '\n'.join(open(path).readlines())))


def graph(data, x_labels, bar_labels, y_label, pdf_name):
    patterns = [ "\\\\\\" , "///" , "+++" , "xxx", "OOO" ]
    import matplotlib as mpl
    mpl.use('Agg')# to avoid warning if x-server is not available
    import matplotlib.pyplot as plt
    plt.style.use('scripts/rob.mplstyle')
    fig, ax = plt.subplots(figsize=(16,5), dpi=300)
    bar_width = .8/len(data)
    for rowIdx, row in enumerate(data):
        x = [x + bar_width *rowIdx -.3 for x in range(len(data[0]))]
        #ax.bar(x, row, bar_width, label=bar_labels[rowIdx], hatch=patterns[rowIdx], edgecolor='black')
        ax.bar(x, row, bar_width, label=bar_labels[rowIdx])

    ax.set_xticks(range(len(data[0])))
    ax.set_xticklabels(x_labels, rotation=45, ha='right', rotation_mode='anchor')
    ax.set_ylabel(y_label)
    ax.set_xlim((-.5,len(data[0]) - .5))
    ax.set_ylim((0,.2))

    ax.plot([5.5,5.5],[-1,1], color='black', linestyle='dashed')
    ax.plot([13.5,13.5],[-1,1], color='black', linestyle='dashed')
    plt.text(1.5, 0.21, "Closed class", ha='left', fontsize='large')
    plt.text(8.5, 0.21, "Open class", ha='left', fontsize='large')
    plt.text(14.7, 0.21, "Other", ha='left', fontsize='large')
    if len(''.join(bar_labels)) > 0:
        leg = ax.legend()
        leg.get_frame().set_linewidth(1.5)
    fig.savefig(pdf_name, bbox_inches='tight')

