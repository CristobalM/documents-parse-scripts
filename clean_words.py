import re
import unidecode
import os
import sys
import argparse

remove_chars_regex = r'\W'


def clean_word(word):
    parsed_word = unidecode.unidecode(word)
    parsed_word = re.sub(remove_chars_regex, '', parsed_word)
    return parsed_word


word_regex_str = r'([^\s]+)'
word_regex_c = re.compile(word_regex_str)

html_tags_regex_c = re.compile('<.*?>')

html_bad_patterns = [
        '&[rl]dquo;',
        '&[rl]squo;',
        '&nbsp;'
    ]


def remove_html_tags(text):
    out = re.sub(html_tags_regex_c, '', text)
    for bad_pattern in html_bad_patterns:
        out = re.sub(bad_pattern, '', out)
    return out


def clean_line(line_in):
    line = remove_html_tags(line_in)
    line = re.sub(r'\s+', ' ', line)
    # line = re.sub(r'[0-9]+', '', line)
    line = re.sub(r'[^a-zA-Z\s]+', '', line).lower()
    word_matches = word_regex_c.findall(line)
    counter = 0
    if len(word_matches) == 0:
        return None

    word_list = []
    for raw_word in word_matches:
        counter += 1
        word = clean_word(raw_word)
        if len(word) == 0:
            continue

        word_list.append(word)

    return word_list

def clean_file(file_path, result_file_location):
    head_orig, tail_orig = os.path.split(file_path)
    file_name_wout_ext, ext = os.path.splitext(tail_orig)
    base_result_location_head, _ = os.path.split(result_file_location)
    result_fname = file_name_wout_ext + "_result" + ext
    result_location = os.path.join(base_result_location_head, result_fname)
    with open(file_path, 'r', encoding="utf8", errors='ignore') as f, open(result_location, 'w') as rf:
        for line_r in f:
            line = remove_html_tags(line_r)
            line = re.sub(r'\s+', ' ', line)
            #line = re.sub(r'[0-9]+', '', line)
            line = re.sub(r'[^a-zA-Z\s]+', '', line).lower()
            word_matches = word_regex_c.findall(line)
            counter = 0
            if len(word_matches) == 0:
                continue
            for raw_word in word_matches:
                counter += 1
                word = clean_word(raw_word)
                if len(word) == 0:
                    continue

                if counter < len(word_matches):
                    rf.write(word + " ")
                else:
                    rf.write(word)

            rf.write('\n')


parser = argparse.ArgumentParser(description='Clean words in documents.')


parser.add_argument('input_path', type=str,  help='Input path, can be a directory with documents or a file (default)')
parser.add_argument('output_path', type=str,  help='Output path, must be a directory')
parser.add_argument('--pisa_format', action="store_true", dest="pisa_format", default=False)

args = parser.parse_args()

print("input_path: " + args.input_path)

is_file = os.path.isfile(args.input_path)
is_dir = os.path.isdir(args.input_path)
is_dir_output_path = os.path.isdir(args.output_path)

if not is_file and not is_dir:
    print(args.input_path + " is not a file or directory")
    exit(1)

if not is_dir_output_path:
    print(is_dir_output_path + " is not a directory")
    exit(1)


if is_file:
    clean_file(args.input_path, args.output_path)

elif is_dir:
    files_in_dir = []

    for file_name in os.listdir(args.input_path):
        file_path = os.path.join(args.input_path, file_name)
        if os.path.isfile(file_path):
            files_in_dir.append(file_path)

    if args.pisa_format:
        print("with pisa format")
        output_file_pisa = os.path.join(args.output_path, 'pisa_format_result.txt')
        with open(output_file_pisa, 'w') as pisa_f:
            counter = 0
            for file_path in files_in_dir:
                if not args.pisa_format:
                    clean_file(file_path, args.output_path)
                else:
                    file_name = os.path.basename(file_path)
                    file_name = re.sub(r'\s', '#', file_name)
                    all_words = []
                    with open(file_path, 'r',  encoding="utf8", errors='ignore') as f:
                        for line in f:
                            line_words = clean_line(line)
                            if line_words is None:
                                continue

                            all_words = all_words + line_words

                    pisa_f.write(file_name + ' ' + ' '.join(all_words) + '\n')
    else:
        for file_path in files_in_dir:
            clean_file(file_path, args.output_path)


