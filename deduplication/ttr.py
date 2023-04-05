#!/usr/bin/python3

import sys

def get_token_statistics(comments):
    token_count = 0
    unique_words = set()    # text only
    unique_symbols = set()  # symbols and emojis (including @username)
    unique_all = set()      # all unique tokens

    for c in comments:
        if c == '\n':
            continue
        tokens = c.split(' ')
        for tok in tokens:
            tok = tok.strip()
            # if tok == '@username':
            #     continue
            token_count += 1
            unique_all.add(tok.lower())
            if any(char.isalnum() for char in tok.strip()) and '@' not in tok:  # token is a word
                    unique_words.add(tok.lower())
            else:   # token is a symbol, an emoji or @username
                unique_symbols.add(tok)

    # for tok in unique_symbols:
    #     print(tok)

    # for tok in unique_words:
    #     print(tok)

    ttr = len(unique_all)/token_count

    return token_count, len(unique_all), len(unique_words), len(unique_symbols), ttr

def main():
    with open(sys.argv[1], 'r', encoding='utf-8') as allcomments:
        comments = allcomments.readlines()

    token_count, num_unique_all, num_unique_words, num_unique_symbols, ttr = get_token_statistics(comments)

    print('Total number of tokens: ' + str(token_count))
    print('Total unique tokens: ' + str(num_unique_all))
    print('Unique word tokens: ' + str(num_unique_words))
    print('Unique symbol tokens: ' + str(num_unique_symbols))
    print('TTR: ' + str(round(ttr, 4)))


if __name__ == '__main__':
    main()