#!/usr/bin/env python3
"""
found_pattern.py

Identify start and end word indices for the CEFRJ Grammatical Items in a Single String

Usage:
python found_pattern.py [REGEX_FILE] "[INPUT_TEXT]"

Example:
python found_pattern.py CEFRJ_grammar_profile_full_20200220.csv "I have been studying English since last year."

Description:
1. Reads regex patterns from a file (e.g., CEFRJ_grammar_profile_full_20200220.csv).
2. Receives a single string as input.
3. Counts how many times each pattern appears in the input string, ignoring case.
4. Stores the counts in a dictionary, mapping pattern_id (1-based) to the frequency count.
"""

import sys
import pandas as pd
import regex
import copy
import process_text

regex_file = "/Users/su-youn.yoon/Scripts/CEFR_grammar_detection/CEFRJ_annotator/CEFRJ_grammar_profile_full_20200220.csv"


class PatternItem:
    def __init__(self, pattern_id, regex):
        """
        Initializes the PatternItem with required fields,
        and sets all other properties to None by default.

        :param pattern_id: Identifier for this pattern.
        :param regex: Regular expression string used by this pattern.
        """
        # Required upon initialization
        self.pattern_id = pattern_id
        self.regex = regex
        # Properties set to None by default (can be assigned later)
        self.explanation = None
        self.sentence_type = None
        self.start_word_index = None
        self.end_word_index = None
        self.actual_string = None

    def __repr__(self):
        """
        Returns a string representation that includes
        pattern_id, grammatical_item, start_word_index,
        end_word_index, and actual_string.
        """
        return (f"PatternItem("
                f"pattern_id={self.pattern_id}, "
                f"explanation={self.explanation}, "
                f"start_word_index={self.start_word_index}, "
                f"end_word_index={self.end_word_index}, "
                f"actual_string={self.actual_string}"
                f")")
def load_regex_patterns(regex_file):
    # Read all regex patterns from the provided file.
    regexes = []
    try:
        df = pd.read_csv(regex_file, dtype=str, keep_default_na=False)
        ids = df.index.tolist()
        for idx in ids:
            regex = df.loc[idx, 'regex']
            pattern_id = df.loc[idx, 'pattern_id']
            pattern = PatternItem(pattern_id, regex)
            pattern.explanation = df.loc[idx, 'grammatical_item']
            regexes.append(pattern)
    except IOError:
        print(f"Could not open {regex_file}. Please make sure the file exists or check permissions.")
        sys.exit(1)
    return regexes

def remove_tags_and_map_intervals(text):
   
    # We'll store:
    #   cleaned_line:   [str, str, ...]  each is a line with tags removed
    #   word_intervals:  [list_of_tuples, ...]
    # where each element of word_intervals[i] is a tuple (start, end) in the
    # original text that maps to the visible text of cleaned_words[i].
  
    # Split into lines.
    lines = text.split('\n')
   
    cleaned_line = []
    word_intervals = []

    current_pos = 0
    for line in lines:
        if len(line) > 0:
           # line including only xml tag
           last_pos = current_pos + len(line)
           if (line[0] == '<') and (line[-1] == '>'):
              pass
           else:
              word_intervals.append((current_pos, last_pos))
              cleaned_line.append(line)
           current_pos = last_pos + 1
    return word_intervals, cleaned_line

def find_word_index_for_char(char_index, word_intervals):
    """
    Given a character index in the original text,
    return which word (0-based) it falls into, or None if it
    is in removed text or beyond all intervals.
    """
    for word_idx, intervals in enumerate(word_intervals):
        start_i, end_i = intervals
        if start_i <= char_index <= end_i:
            return word_idx
    return None

def find_word_indices(start_char_index, end_char_index, word_intervals):
    """
    determine which word the original start_char_index and
    end_char_index fall in (or None if they fall inside removed text
    or in a skipped line).
    Returns:
        (start_word_index, end_word_index)
    """
    # Determine which word (if any) the start_char_index and end_char_index map to
    start_word_index = find_word_index_for_char(start_char_index, word_intervals)
    end_word_index = find_word_index_for_char(end_char_index, word_intervals)
    return (start_word_index, end_word_index)

def get_words_between_indices(word_list, start_word_index, end_word_index):
    # Check if indices are out of bounds
    if start_word_index < 0 or end_word_index >= len(word_list) or start_word_index > end_word_index:
        return None
    # Get the words between the indices and join them into a string
    return ' '.join(word_list[start_word_index:end_word_index + 1])

def get_pattern_and_span(input_text, tagged_text, regexes):
    """
    Given an input_text and a list of regex patterns,
    return a dictionary:
    {
        pattern_id: [(start_index, end_index), (start_index, end_index), ...],
        ...
    }
    using the regex library (PCRE-compatible) with IGNORECASE.
    """
    pattern_spans = {}
    word_list= input_text.split()

    # get cleaned line after removing xml tags and map intervals
    word_intervals, cleaned_line = remove_tags_and_map_intervals(tagged_text)

    for pattern in regexes:
        matches = []
        # Find all matches with start and end indices

        for match in regex.finditer(pattern.regex, tagged_text, flags=regex.IGNORECASE):
            current_pattern = copy.deepcopy(pattern)
            start_char_index = match.start()
            end_char_index = match.end()
            current_pattern.start_word_index, current_pattern.end_word_index = find_word_indices(start_char_index, end_char_index, word_intervals)
            current_pattern.actual_string = get_words_between_indices(word_list, current_pattern.start_word_index, current_pattern.end_word_index)
            print('actual string', current_pattern.actual_string)
            matches.append(current_pattern)
        if len(matches) > 0:
            print('matches', matches)
            pattern_spans[pattern.pattern_id] = matches
    return pattern_spans


def test():
    input_text = "I was reading a book."
    tagged_text = "<file>\nI_PP_I\nwas_VBD_be\nreading_VBG_read\na_DT_a book_NN_book\n._SENT_.\n</file>"
    #tagged_text = "<file>\n<NC>\nI_PP_I\n</NC>\n<VC>\nwas_VBD_be\nreading_VBG_read\n</VC>\n<NC>\na_DT_a book_NN_book\n</NC>\n._SENT_.\n</file>"
    regexes = load_regex_patterns(regex_file)
    tagged_text = process_text.process_one(input_text)
    pattern_spans = get_pattern_and_span(input_text, tagged_text, regexes)


test()
