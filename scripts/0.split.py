import copy
import sys
out_orig = open(sys.argv[1] + '-orig', 'w')
out_norm = open(sys.argv[1] + '-norm', 'w')

for line in open(sys.argv[1]):
    if len(line) < 3 or line[0] == '#':
        out_orig.write(line)
        out_norm.write(line)
    else:
        orig_tok = line.strip().split('\t')
        if ' ' in orig_tok[3]:
            orig_tok[3] = orig_tok[3].split()[0]
        out_orig.write('\t'.join(orig_tok) + '\n')

        norm_tok = line.strip().split('\t')
        if ' ' in norm_tok[2]:
            tags = norm_tok[3].split(' ')[1].split('|')
            words = norm_tok[2].split(' ')
            for tag, word in zip(tags, words):
                tag = tag.replace('(', '').replace(')', '')
                out_norm.write('\t'.join(['_', word, '_', tag, norm_tok[4], norm_tok[5]]) + '\n')
                print('\t'.join(['_', word, '_', tag, norm_tok[4], norm_tok[5]]))
        elif norm_tok[2] == '':
            continue
        else:
            norm_tok[1] = norm_tok[2]
            norm_tok[2] = '_'
            out_norm.write('\t'.join(norm_tok) + '\n')
        

out_orig.close()
out_norm.close()

