# dow_anagram_phrases
Find anagram phrases of day of week names. E.g., 'monday' --> 'yam nod'.

The resulting files from running `python dow_anagram_phrases.py --dict_path /usr/share/dict/words` are the text files included. `/usr/share/dict/words` is the default path of the dictionary being used. If this does not exist for you, provide a path to a line separated text file that you want to use as a dictionary for filtering out strings which are not words using `--dict_path <path_to__file>`.