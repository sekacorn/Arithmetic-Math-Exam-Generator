# Arithmetic & Algebra Exam Generator

Greetings Jolly educator! This Python application helps you create **randomized** arithmetic Exam in LaTeX format.
 It can generate questions tailored to various grade levels (1–3, 4, 4–6, and 6–7). Plus, it now prompts you to **optionally include algebra questions**, giving your students the perfect challenge when they’re ready for it.  

The script automatically creates two `.tex` files:
1. **`questions.tex`** – where all your test questions appear.  
2. **`answers.tex`** – an answer key, making it easy to check student work.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Customization](#customization)  
- [Output Files](#output-files)  
- [Contributing](#contributing)  
- [License](#license)

---

## Overview

This tool is designed for elementary to junior high math levels. It randomly generates a variety of problem types:

- **Addition**  if you choose to include it)
- **Subtraction**  if you choose to include it)
- **Division**   if you choose to include it)
- **Fraction Multiplication**  if you choose to include it)
- **Algebra** (if you choose to include it)

Each question is placed into a neatly formatted LaTeX document, along with a matching solution file.

---

## Features

1. **Math-Grade-Level Range**: 
   - **1st to 3rd Grade level Math** (simple addition and subtraction, can also include algebra if chosen)  
   - **4th Grade level Math** (addition, subtraction, division, can also include algebra if chosen)  
   - **5th to 6th Grade level Math** (addition, subtraction, division, fraction multiplication. can also include algebra if chosen)  
   - **6th to 7th Grade level Math** (“hard,” can also include algebra if chosen)

2. **Algebra Prompt**:  
   - **Optional**: Choose whether to add algebra questions specifically for 6th–7th grade or keep it at standard arithmetic.

3. **Randomized Questions**:  
   - No test will look the same, saving time in test creation and reducing the chance of students sharing answers from previous tests.

4. **Points Per Question**:  
   - Customize how many points each question is worth.

5. **Extra Space for Work**:  
   - If an algebra question is generated, the `.tex` file automatically includes added vertical space for showing calculations.

---

## Prerequisites

- **Python 3.6+**  
- A **LaTeX distribution** (like TeX Live or MiKTeX) if you want to compile the `.tex` files into PDFs.  
- Basic Python libraries (`random`, `os`, `math`)—no additional external libraries needed.
- An online website with Free tex to PDF converter tool

---

## Installation

1. **Clone or Download** this repository to your local machine.
2. **Check Python**:
   ```bash
   python --version
   ```
---

## Usage
Navigate to the directory where the files are located in your terminal or command prompt.

Run the script:

```bash
	python Generate_Arithmetic_Math_Exam.py
 ```
Follow the prompts:

 1. Enter the desired difficulty level (1-3, 4, 4-6, or 6-7).
 2. Specify the total number of questions.
 3. State how many points each question should be worth.
 4. After that, the program automatically creates two files in the current directory:

---

## Output Files
  ```bash
	  questions.tex
	  answers.tex
  ```


Contains a LaTeX preamble (including \documentclass and packages like amsmath).
Lists each question in an enumerated format.
Displays the difficulty level, total questions, and points per question at the top.
answers.tex

Mirrors the structure of questions.tex but provides correct answers in place of the questions.
To convert these into PDFs, simply run:

```bash
pdflatex questions.tex
pdflatex answers.tex
```
Or you can use free online '.tex to PDF' conversion tools from the internet to convert the two .txt files to human legible PDF file
---

## Customization
	- Difficulty Ranges: Adjust the numeric range for each difficulty level in the generate_problem function.
	- Operations: Edit the operations list (add multiplication, exponentiation, etc.).
	- Question Phrasing: Modify the question text or instructions in the LaTeX content sections for a more personal touch.

---

## Troubleshooting
	- LaTeX errors: Ensure \usepackage{amsmath} is present and your LaTeX distribution is up to date.
	- ZeroDivisionError or unusual generation: Check that the numeric ranges are set correctly and that you are generating questions appropriate for your difficulty level.
	- Python environment issues: Confirm you’re using Python 3.6 or above and that you can run Python scripts in your current environment.
	
---

## License
	This project is licensed under the MIT License. Feel free to use, modify, and distribute it. If it brings you a little extra peace and clarity in your day, and for
	mankind.



