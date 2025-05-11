# CEFR Grammatical Expression Detector

This repository contains a Python script designed to detect CEFR (Common European Framework of Reference for Languages) grammatical expressions in text. For each sentence processed, the script provides a list of CEFR-J grammatical expressions along with their spans (start and end word indices). The original code was developed by [CEFR-J](https://cefr-j.org/cefrj.html) in perl. It has been translated from Perl to Python, utilizing the same regular expression lists for detecting CEFR grammatical expressions.

## Features

- Detects CEFR-J grammatical expressions in text.
- Provides the pattern id, a brief English explanation, and span (start and end word indices) for each detected expression.

## Installation

**1. Install TreeTagger**   
- Install treetagger from https://www.tufs.ac.jp/ts/personal/corpuskun/wiki/index.php?TreeTagger. The details of TreeTagger installing is explained in the end of this NOTE section in this README.

**2. Install CEFR detector**
- clone this repository.
- Update the following two paths


## Usage

To use the script, run the following command:

```bash
python detect_cefr_expressions.py <input_file>
``


## NOTES

**. Detailed Tips about TreeTagger installation.
- You need to download Penn Tagset. 
- From your TreeTagger directory, check the shell script ./cmd/tree-tagger-english and comment the last two lines:
# perl -pe 's/\tV[BDHV]/\VB/;s/IN\/that/\tIN/;'
# --> perl -pe 's/IN\/that/\tIN/;' 

e.g., example of TreeTagger output:
echo 'I was reading a book.' | cmd/tagger-chunker-english
I	PP	I
was	VBD	be
reading	VVG	read
a	DT	a
book	NN	book
.	SENT	.
	 finished.
[NOTE] the POS of reading is "VVG" not "VBD". CEFRJ regular expression is based on the "VVG" not "VBD". 





## Usage

To use the script, run the following command:

```bash
python detect_cefr_expressions.py <input_file>
```

- `<input_file>`: Path to the csv file containing pairs of a sentence_id and a sentence to be analyzed.

The script will output the detected CEFR-J grammatical expressions and their spans for each sentence in the input file.

## Example

Suppose you have a text file `sentences.csv` with the following content:

```
s01, "I have been to London."
s02, "She is reading a book."
```

Running the script:

```bash
python detect_cefr_expressions.py sentences.csv
```

Output:
sentence_id, [(cefr_id, 'expression_str', (start_id, end_id'), ...]

```
001,[('have been', (1, 3))]
```

## Acknowledgments

- Original Perl scripts and regular expression lists by [CEFR-J](https://cefr-j.org/cefrj.html).
- Thanks to the CEFR-J team for their foundational work in developing the grammatical expression detection framework.

# CEFRJ_annotator
