import process_text
import json
from pathlib import Path
import sys
import find_pattern
import re


def apply_edits(original_tokens, edits):
    """
    Given a list of tokens and a list of edits (start, end, replacement),
    produce a corrected list of tokens. We apply the edits in descending
    order of the start index so that the token indices do not get shifted
    for subsequent edits.
    """
    # Sort edits by their start index (descending)
    edits_sorted = sorted(edits, key=lambda e: e[0], reverse=True)
    tokens = original_tokens[:]
    for start, end, replacement in edits_sorted:
        # Replace tokens in [start:end] with replacement tokens
        tokens = tokens[:start] + replacement + tokens[end:]
    return tokens

def parse_m2_file(m2_path):
    """
    Generator that yields (original_sentence_tokens, list_of_edits)
    for each sentence in the M2 file.
    """
    with open(m2_path, "r", encoding="utf-8") as f:
        orig_tokens = None
        edits = []

        for line in f:
            line = line.strip()
            # Skip empty lines (sentence boundary or end of file)
            if not line:
                # If we have an accumulated sentence, yield it
                if orig_tokens is not None:
                    yield orig_tokens, edits
                # Reset for next sentence
                orig_tokens = None
                edits = []
                continue

            if line.startswith("S "):
                # Start of a new sentence
                # Example: S My friend are nice .
                # Remove leading "S " and split on whitespace
                x = line.split()
                sentence_str = ' '.join(x[1:])
                orig_tokens = sentence_str.split()

            elif line.startswith("A "):
                # Annotation line with format:
                # A start end|||error_type|||replacement_text|||...
                # Example: A 1 2|||R:VERB_AGR|||is|||REQUIRED|||-NONE-|||
                # We only need start, end, and replacement
                # Typically: A start end|||...|||replacement|||(other fields)
                ann_parts = line.split("|||")
                # The left part (before the first "|||") has "A start end"
                left_part = ann_parts[0]
                # Example left_part: "A 1 2"
                # The replacement is ann_parts[2].
                replacement_str = ann_parts[2].strip()
                # The final field after the last "|||" is the alternative index
                # For instance, "...|||0" => alt_index = "0"
                alt_index = ann_parts[-1].strip()

                # Skip if it is not the alternative "0"
                if alt_index != "0":
                    continue
                # The numeric indices are after "A "
                # e.g., "A 1 2" -> start=1, end=2
                match = re.match(r"A\s+(\d+)\s+(\d+)", left_part)
                if not match:
                    continue
                start_idx = int(match.group(1))
                end_idx   = int(match.group(2))

                # Split replacement on whitespace (handle empty or "-NONE-")
                if replacement_str == "-NONE-":
                    replacement_tokens = []
                else:
                    replacement_tokens = replacement_str.split()

                edits.append((start_idx, end_idx, replacement_tokens))

        # If file doesn't end with a blank line, yield the last one.
        if orig_tokens is not None:
            yield orig_tokens, edits

def test(m2_file):
    for orig_tokens, edits in parse_m2_file(m2_file):
        corrected_tokens = apply_edits(orig_tokens, edits)
        corrected_sentence = " ".join(corrected_tokens)
        print("Original:  " + " ".join(orig_tokens))
        print("Corrected: " + corrected_sentence)
        print()  # blank line between sentences

def process_ctseg(indir, outdir):
    """
    1. Lists all .md files in the 'indir'.
    2. Extracts original sentences from each .md file.
    3. Writes the sentences into a JSON file in 'outdir', using the same
    base file name (but .json extension).
    """
    # Ensure output directory exists
    regex_file = "/Users/su-youn.yoon/Scripts/CEFR_grammar_detection/CEFRJ_annotator/CEFRJ_grammar_profile_full_20200220.csv"

    outdir_path = Path(outdir)
    outdir_path.mkdir(parents=True, exist_ok=True)

    # load regular expression patterns for CEFR detection
    regexes = find_pattern.load_regex_patterns(regex_file)

    # Find all .md files in the input directory
    for m2_path in Path(indir).glob("*.m2"):
        print('processing------------------', m2_path
        )
        data = {"sentences": []}
        sentences = []
        for orig_tokens, edits in parse_m2_file(m2_path):
            corrected_tokens = apply_edits(orig_tokens, edits)
            corrected_sentence = " ".join(corrected_tokens)
            sentences.append(corrected_sentence)
        for i, s in enumerate(sentences):
            tagged_sentence = process_text.run_text_procesesor(s)
            annotated_sentence = find_pattern.get_pattern_and_span(s, tagged_sentence, regexes)
            data['sentences'].append({'original_sentence': s,
                                      'tagged_sentence': tagged_sentence,
                                      'CEFRJ_annotation': annotated_sentence})

        # Build output JSON filename with same stem as the .md file
        out_json_path = outdir_path / (m2_path.stem + ".json")

        # Write data to JSON file
        with open(out_json_path, "w", encoding="utf-8") as out_file:
            output = json.dumps(data,  ensure_ascii=True, indent=2)
            out_file.write(output)


        print(f"Created JSON file: {out_json_path}")
 

def main():
    """
    Example usage:
    python script_name.py /path/to/input /path/to/output
    """
    #if len(sys.argv) < 3:
    #    print("Usage: python script_name.py <indir> <outdir>")
    #    sys.exit(1)

    indir = '/Users/su-youn.yoon/Scripts/CEFR_grammar_detection/CTSEG'
    outdir = '/Users/su-youn.yoon/Scripts/CEFR_grammar_detection/CTSEG/CEFR_annotated_sentences'
    process_ctseg(indir, outdir)

main()