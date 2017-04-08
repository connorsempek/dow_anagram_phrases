###############################################################################
### Day of Week Anagrams                                                    ###
### Code to create all n-word anagrams from names of days of the week       ###
###############################################################################


# -----------------------------------------------------------------------------
# imports

import argparse
import datetime as dt
import itertools
import operator
import sys
import timeit


# -----------------------------------------------------------------------------
# helper functions

def is_strictly_increasing(x):
    '''determine if an array contains strictly increasing items
    '''
    
    res = True
    for i in range(len(x) - 1):
        if x[i] >= x[i + 1]:
            res = False
            break
    return res


def permute_string(s):
    '''returns a list of all permutation of a string
    '''
    
    return list(set([''.join(perm) for perm in itertools.permutations(s)]))


def strictly_increasing_tups(s, n):
    
    vals = [range(i + 1, len(s)) for i in range(n)]
    prod = itertools.product(*vals)
    return [tup for tup in prod if is_strictly_increasing(tup)]


def all_strictly_increasing_tups(s):
    
    tups = []
    for n in range(len(s)):
        tups += strictly_increasing_tups(s, n)
    return tups


def split_string_by_tup(s, tup):

    res = []
    if tup:
        for i in range(len(tup)):
            if i == 0:
                res.append(s[:tup[i]])
            elif 0 < i <= len(tup) - 1:
                res.append(s[tup[i - 1]:tup[i]])
            if i == len(tup) - 1:
                res.append(s[tup[i]:])
    else:
        res.append(s)
    return res


def all_string_phrases(s, tups):
    
    phrases = []
    for tup in tups:
        phrases.append(split_string_by_tup(s, tup))
    return phrases


def all_anagram_phrases(s, tups):
    
    phrases = []
    perms = permute_string(s)
    n = 1.0 * len(perms)
    for i, perm in enumerate(perms):
        sys.stdout.write('\r')
        phrases += all_string_phrases(perm, tups)
        sys.stdout.write('{:.2%}'.format((i + 1) / n))
        sys.stdout.flush()
    return phrases


def load_dictionary(dict_path='/usr/share/dict/words'):

    # read in dictionary
    with open(dict_path, 'r') as f:
        dictionary = f.readlines()
    dictionary = set([w.lower().strip() for w in dictionary])

    # remove non-word single letters
    if dict_path == '/usr/share/dict/words':
        good_singles = set(['a', 'i', 'o'])
        bad_singles = set([w for w in dictionary if len(w) == 1 and w not in good_singles])
        dictionary = set([w for w in dictionary if w not in bad_singles]) 

    return dictionary


def is_phrase_legit(phrase, dictionary):
    
    res = True
    for w in phrase:
        if w not in dictionary:
            res = False
            break
    return res


def dedupe_phrases(phrases):
    
    sorted_phrases = set([','.join(sorted(p)) for p in phrases])
    return [p.split(',') for p in sorted_phrases]


def get_legit_anagram_phrases(s, dictionary):
    
    tups = all_strictly_increasing_tups(s)
    phrases = all_anagram_phrases(s, tups)
    phrases = [p for p in phrases if is_phrase_legit(p, dictionary)]
    return dedupe_phrases(phrases)

# -----------------------------------------------------------------------------
# find anagram phrases for each day of week name and write to text file

if __name__  == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dict_path', help='file path to dictionary', 
        type=str, default='/usr/share/dict/words')
    args = parser.parse_args()

    # get day names
    dows = [(dt.date.today() + dt.timedelta(days=i)).strftime('%A').lower()
            for i in range(7)]

    # load simple english dictionary
    dictionary = load_dictionary(args.dict_path)

    # find anagram phrases and write to text find for each day name
    for dow in dows:
        
        sys.stdout.write('\n')
        sys.stdout.write('Finding anagram phrases for {} ...'.format(dow))
        sys.stdout.write('\n')
        
        # get all english anagram phrases for the day name
        phrases = get_legit_anagram_phrases(dow, dictionary)
        
        sys.stdout.write('\n')
        sys.stdout.write('    complete')
        sys.stdout.write('\n')
        
        sys.stdout.write('\n')
        fn = '{}_anagram_phrases.txt'.format(dow)
        sys.stdout.write('Writing anagram phrases of {} to {} ...'.format(dow.title(), fn))
        sys.stdout.write('\n')
        
        # write to text file
        with open(fn, 'w') as f:
            for p in phrases:
                f.write(', '.join(p) + '\n')
        
        sys.stdout.write('\n')
        sys.stdout.write('    complete')
        sys.stdout.write('\n')            


        sys.stdout.write('\n')
        sys.stdout.write('There are {} anagram phrases for {}'.format(len(phrases), dow.title()))
        sys.stdout.write('\n')
        sys.stdout.write('\n')
