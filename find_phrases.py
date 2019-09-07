import os
import argparse
import re
import random
import math

word_regex_str = r'([^\s]+)'
word_regex_c = re.compile(word_regex_str)


def list_files(directory_path):
    files_in_dir = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            files_in_dir.append(file_path)

    return files_in_dir


def find_phrases_in_directory(directory_path, number_of_phrases, phrase_words=3):
    files_in_dir = list_files(directory_path)
    files_qty = len(files_in_dir)
    phrases_per_file = int(math.ceil(number_of_phrases / files_qty))
    print("Phrases per file %i" % phrases_per_file)
    search_depth = 100

    phrases_output = []

    found_phrases = False

    for file_path in files_in_dir:
        with open(file_path) as f:
            file_content = f.read()
            words_in_file = word_regex_c.findall(file_content)
            words_in_file_len = len(words_in_file)
            selected_indexes = {}
            search_bound = words_in_file_len - 1 - phrase_words
            if search_bound < 0:
                print("SEARCH BOUND < 0 for file path: " + file_path)
                exit(2)
            for i in range(0, phrases_per_file):
                found_new_val = False
                for j in range(0, search_depth):
                    random_val = random.randint(0, search_bound)
                    if random_val not in selected_indexes:
                        selected_indexes[random_val] = True
                        found_new_val = True
                        break
                if not found_new_val:
                    print("COULDN'T FIND NEW VAL IN FILE PATH : " + file_path)
                    exit(3)

            for first_idx in selected_indexes.keys():
                phrase = []

                for i in range(first_idx, first_idx + phrase_words):
                    phrase.append(words_in_file[i])

                phrases_output.append(phrase)
                if len(phrases_output) >= number_of_phrases:
                    found_phrases = True
                    break

            if found_phrases:
                break

    return phrases_output


parser = argparse.ArgumentParser(description='Find phrases')
parser.add_argument('input_directory_path', type=str, help='Directory path that has documents')
parser.add_argument('number_of_phrases', type=str, help='Number of phrases')
parser.add_argument('output_file', type=str, help='Output file')
args = parser.parse_args()

if not os.path.isdir(args.input_directory_path):
    print(args.input_directory_path + " is not a directory")
    exit(1)

list_of_phrases = find_phrases_in_directory(args.input_directory_path, int(args.number_of_phrases))

with open(args.output_file, 'w') as f:
    for phrase_list in list_of_phrases:
        #print(' '.join(phrase_list))
        f.write(' '.join(phrase_list) + '\n')


