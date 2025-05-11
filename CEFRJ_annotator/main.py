import os
import configparser
import process_text
import find_pattern

def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    regex_file = config["Paths"]["regex_file"]
    tree_tagger_cmd = config["Paths"]["tree_tagger_cmd"]
    return regex_file, tree_tagger_cmd

def main(config_path, input_text):
    regex_file, tree_tagger_cmd = load_config(config_path)
    #input_text = "why do n't you want to join our club ?"
    regexes = find_pattern.load_regex_patterns(regex_file)
    tagged_sentence = process_text.run_text_procesesor(input_text, tree_tagger_cmd)
    annotated_sentence = find_pattern.get_pattern_and_span(input_text, tagged_sentence, regexes)
    print('input_text:', input_text)
    print('annotated_sentence', annotated_sentence)

if __name__ == '__main__':
    import sys
    
    config_path = sys.argv[1]
    input_text = sys.argv[2]
    main(config_path, input_text)