# Homework Grading Assistant Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)

## What This Tool Does
This automated system helps:
1. Track which students submitted homework
2. Assign graders fairly
3. Create organized grading lists

## Key Features
- Scrapes submissions list from any website that has tables (eg. quera.org)
- Handles persian and english student numbers
- Distributes grading work equally and randomly
- Creates ready-to-use grading lists
- Flexible command-line options
---

## Get Started (linux)

### 1. Download the Tool
```bash
git clone git@github.com:pouyatavakoli/GraderAssigner.git
cd GraderAssigner
```

### 2. Setup Python Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Prepare Your Files
Create these files in the project folder:

**students.csv** (student list)

keep the header as the example below

you can also export Comma-separated values (CSV) from any platform (eg. google sheets) and paste it here but remember to fix the headers

**pro tip:** for persian names the headers may seem to be in wrong order when exporting as csv don't change it, let it be is it is!

```csv
student_number,student_name
12345,name 2
54321,name 2
```

**graders.txt** (who will grade)

write one name per line

```text
grader_1
grader_2
```

**submitted.json** (who submitted - you'll create this next using the scrape.js script)

the file content should look like this in the end
```json
["12345", "112233"]
```

---

## How to Use It

### Step 1: Get Submission Data (firefox)
1. Open the homework submissions page in your browser
2. Press `Ctrl+Shift+i` (Windows/Linux) or `Cmd+Option+i` (Mac)
3. Paste the code from `scrape.js` in the console
4. Press Enter
5. Copy the list of student numbers that appears

### Step 2: Create submitted.json
1. Open submitted.json in a text editor
2. Paste the student numbers you copied
3. Save the file

### Step 3: Run the Tool
```bash
python3 assign_graders.py
```

### Step 4: Get Your Grading List

you can then import this csv in any platform.

Check the new file `grading_assignments.csv`:

```csv
student_number,student_name,submitted,grader
12345,name 1,yes,grader_1
54321,name 2,no,N/A
```

---

## File Guide

| File | Purpose | Format |
|------|---------|--------|
| `students.csv` | Student roster | CSV with headers |
| `graders.txt` | List of graders | One name per line |
| `submitted.json` | Who submitted | List of student numbers |
| `grading_assignments.csv` | Final assignments | CSV with submission status |

---
## Command Line Options
Customize the tool's behavior with these flags:

| Flag | Default Value | Description |
|------|---------------|-------------|
| `--students` | `students.csv` | Path to student roster CSV |
| `--submitted` | `submitted.json` | Path to submission data JSON |
| `--graders` | `graders.txt` | Path to grader list text file |
| `--output` | `grading_assignments.csv` | Output file path |

### Examples:
```bash
# Basic usage
python3 assign_graders.py

# Custom file locations
python assign_graders.py \
  --students class_roster.csv \
  --submitted hw1_submissions.json \
  --graders teaching_assistants.txt \
  --output hw1_assignments.csv
```

--- 

## Custom Options

### Use Different Filenames
```bash
python3 assign_graders.py \
  --students my_class.csv \
  --graders teaching_team.txt \
  --output hw1_graders.csv
```

### Check Distribution
The tool automatically balances assignments between graders:
```
grader_1 : 16 students
grader_2 : 15 students
grader_3 : 15 students
```

### Update the Tool
```bash
# Get latest version
git pull origin main

# Update packages
pip install -r requirements.txt
```

---

## Troubleshooting

### Browser Script Issues
- **No student numbers?** 
  1. Right-click the table > "Inspect"
  2. Check column positions
  3. Update in `scrape.js`: `STUDENT_NUMBER_COLUMN = 1` (this is zero indexed write 1 for 2nd column)


- **Virtual environment problems**
  - Reactivate with: `source .venv/bin/activate` (Linux/Mac)

---
