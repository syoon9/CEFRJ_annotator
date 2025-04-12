# CEFR Grammatical Expression Detector

This repository contains a Python script designed to detect CEFR (Common European Framework of Reference for Languages) grammatical expressions in text. For each sentence processed, the script provides a list of CEFR-J grammatical expressions along with their spans (start and end word indices). The original code was developed by [CEFR-J](https://cefr-j.org/cefrj.html) and has been translated from Perl to Python, utilizing the same regular expression lists for detecting CEFR grammatical expressions.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- Detects CEFR-J grammatical expressions in text.
- Provides the span (start and end word indices) for each detected expression.
- Translated from the original Perl scripts to Python for ease of use and integration.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/cefr-grammatical-expression-detector.git
   cd cefr-grammatical-expression-detector
   ```

2. **Install the required dependencies:**

   Ensure you have Python 3.x installed, then install the necessary packages:

   ```bash
   pip install -r requirements.txt
   ```

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
