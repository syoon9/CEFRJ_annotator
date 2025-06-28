# CEFR Grammatical Expression Detector

This repository contains a Python script designed to detect CEFR (Common European Framework of Reference for Languages) grammatical expressions in text. For each sentence processed, the script provides a list of CEFR-J grammatical expressions along with their spans (start and end word indices). The original code was developed by [CEFR-J](https://cefr-j.org/cefrj.html) in perl. It has been translated from Perl to Python, utilizing the same regular expression lists to detect CEFR grammatical expressions while adding a span detection function. 

## Features

- Detects CEFR-J grammatical expressions in text.
- Provides the pattern id, a brief English explanation, and span (start and end word indices) for each detected expression.

## Installation

**1. Install TreeTagger**   
- Install treetagger from https://www.tufs.ac.jp/ts/personal/corpuskun/wiki/index.php?TreeTagger. The details of TreeTagger installing is explained in the end of this NOTE section in this README.

**2. Install CEFR detector**
- clone this repository.
- Update the following two paths in config.ini: regex_file, tree_tagger_cmd


## Usage

To use the script, run the following command:

python main.py your_config_path your_tokenized_input_text

e.g., main.py config.ini "Why do n't you join our club ?"


## Acknowledgments

- Original Perl scripts and regular expression lists by [CEFR-J](https://cefr-j.org/cefrj.html).
- Thanks to the CEFR-J team for their foundational work in developing the grammatical expression detection framework.


## NOTES

**. Detailed Tips about TreeTagger installation.
- You need to download Penn Tagset. 
- From your TreeTagger directory, check the shell script ./cmd/tree-tagger-english and comment the following last two lines:  
   perl -pe 's/\tV[BDHV]/\VB/;s/IN\/that/\tIN/;'  
     --> perl -pe 's/IN\/that/\tIN/;' 

Commenting this line will stop you to replace tags 

e.g., example of TreeTagger output:  
echo 'I was reading a book.' | cmd/tagger-chunker-english  
I	PP	I  
was	VBD	be  
reading	VVG	read  
a	DT	a  
book	NN	book  
.	SENT	.  
	 finished.  
[NOTE] the POS of reading should be "VVG" which is the part of BNC taglist, but not "VBG". CEFRJ regular expression is using "VVG" not "VBG". 


