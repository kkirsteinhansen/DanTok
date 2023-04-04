import myutils
import json
import os

# single dataset models
for treebank in myutils.trains:
    train, dev, test = myutils.getTrainDevTest('machamp/data/ud-treebanks-v2.11.singleToken/' + treebank)
    train = train.replace('machamp/', '')
    dev = dev.replace('machamp/', '')
    data_config = {treebank: {'train_data_path': train, 'dev_data_path': dev, 'word_idx': 1}}
    data_config[treebank]['tasks'] = {'UPOS': {'task_type': 'seq', 'column_idx': 3}}
    data_path = 'machamp/configs/' + treebank + '.json'
    json.dump(data_config, open(data_path, 'w'), indent=4)
    for mlm in myutils.mlms:
        mlm_name = mlm.replace('/', '_')
        param_path = 'machamp/configs/params.' + mlm_name
        if not os.path.isfile(param_path):
            param_config = myutils.load_json('machamp/configs/params.json')
            param_config['transformer_model'] = mlm
            json.dump(param_config, open(param_path, 'w'), indent=4)
        name = treebank + '.' + mlm_name
        if myutils.getModel(name) == '':
            cmd = 'python3 train.py --dataset_configs ' + data_path.replace('machamp/', '') + ' --parameters_config ' + param_path.replace('machamp/', '') + ' --name ' + name
            print(cmd)


# multi-dataset model
for mlm in myutils.mlms:
    mlm_name = mlm.replace('/', '_')
    param_path = 'machamp/configs/params.' + mlm_name
    if not os.path.isfile(param_path):
        param_config = myutils.load_json('machamp/configs/params.json')
        param_config['transformer_model'] = mlm
        json.dump(param_config, open(param_path, 'w'), indent=4)
    data_configs = ['configs/' + treebank + '.json' for treebank in myutils.trains[1:]]
    name = '.'.join(myutils.trains[1:]) + '.' + mlm_name
    if myutils.getModel(name) == '':
        cmd = 'python3 train.py --dataset_configs ' + ' '.join(data_configs) + ' --parameters_config ' + param_path.replace('machamp/', '') + ' --name ' + name
        print(cmd)

