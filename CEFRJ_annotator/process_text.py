import re
import subprocess
#import treetaggerwrapper

def preprocess_line(line: str) -> str:
    """
    Apply the same text substitutions as in the Perl script to a single line of text.
    """
    # Replace “ and ” with a double quote
    line = re.sub(r'[“”]', '"', line)
    # Replace ‘, ’, and ` with a single quote
    line = re.sub(r'[‘’`]', "'", line)
    # Replace ， with ", "
    # line = re.sub(r'，', ', ', line)
    # Replace ： with ": "
    line = re.sub(r'：', ': ', line)
    # Replace … with " ..."
    line = re.sub(r'…', ' ...', line)
    # Replace the full-width space (　) or tab with a half-width space
    line = re.sub(r'[　\t]', ' ', line)
    # Replace ～ or ~ with "..."
    line = re.sub(r'[～~]', '...', line)
    return line


def xmlize_single_line(line: str) -> str:
    """
    Process one line of TreeTagger output according to the rules
    that apply strictly at a single-line level.

    1) Remove BOM if present at the start.
    2) If the line is exactly '<g/>', return an empty string (equivalent to skipping it).
    3) If the line starts with '<', return it as-is (other than BOM removal).
    4) Otherwise:
       - Remove trailing '-[acdijmnprvx]' if present (ICNALE-specific).
       - Escape '&', '>', and '<' for XML.
       - Replace tabs ('\t') with underscores ('_').

    Returns the transformed line. If you need to skip the line, it returns an empty string.
    """

    # Strip any trailing newline
    line = line.rstrip('\n')

    # Remove a possible BOM character (\ufeff) at the start (ICNALE-specific)
    line = re.sub(r'^\ufeff', '', line)

    # Skip if exactly <g/>
    if line == "<g/>":
        return ""

    # If the line starts with '<', we return it "as is"
    # (except for having removed any BOM above).
    if line.startswith("<"):
        return line

    # Remove trailing -[acdijmnprvx], if present (ICNALE-specific)
    line = re.sub(r'-[acdijmnprvx]$', '', line)

    # Escape certain special characters for XML
    line = line.replace("&", "&amp;")
    line = line.replace(">", "&gt;")
    line = line.replace("<", "&lt;")

    # Replace tabs with underscores
    line = line.replace("\t", "_")
    return line


def run_treetagger_on_sentence(sentence: str) -> list:
    """
    Runs TreeTagger on a single-sentence string input, capturing and parsing the results.
    Parameters:
    -----------
    sentence : str
        The text you want to process (a single sentence) by TreeTagger.
    tree_tagger_cmd : str
        Command or full path to the TreeTagger executable (e.g., "tree-tagger", "C:/TreeTagger/bin/tag-english", etc.)
    Returns:
    --------
    A list of line with each line including 3 columns (token, pos, lemma)

    Requirements:
    -------------
    1) TreeTagger must be installed on your system.
    2) The tree_tagger_cmd must be valid: either on PATH or an absolute path.
    3) The appropriate parameter or parameter file for language must be integrated
       into the tree_tagger_cmd if needed (e.g., "tree-tagger-english" vs. "tag-english").
    """
    # Prepare a temporary file with the single sentence
    tree_tagger_cmd = '/Users/su-youn.yoon/Scripts/external_resources/CEFRJ_annotation_scripts/TreeTagger/tree-tagger-MacOSX-M1-3.2.3/cmd/tree-tagger-english'
    try:
        # Run the TreeTagger command via subprocess
        # Capture the output in "pipe" mode
        result = subprocess.run(
            [tree_tagger_cmd],
            input=sentence,  # Provide LINE as stdin
            text=True,  # Indicates input/output are strings
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            check=True
        )

        # Parse the output lines:
        # Typical line format from TreeTagger: "word\tPOS\tlemma"
        output = []
        for line in result.stdout.splitlines():
            # Each line has up to three columns
            columns = line.split("\t")
            if len(columns) >= 3:
                output.append(line)
            else:
                # If the line doesn't match the expected format, ignore or handle accordingly
                pass
    except:
        output = None
    return output

def process_one(sentence: str) -> str:
    processed_sentence = preprocess_line(sentence)
    tagged_sentence = run_treetagger_on_sentence(processed_sentence)
    processed_sentence = xmlize_single_line('\n'.join(tagged_sentence))
    return processed_sentence


def test():
    input_text = "I was reading a book."
    print(process_one(input_text))

   # xmlized_text = xmlize_single_line(tagged_text)



test()
