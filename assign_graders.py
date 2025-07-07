#!/usr/bin/env python3

import json
import csv
import numpy as np
import pandas as pd
from collections import defaultdict
import argparse

def main():
    # command-line arguments
    parser = argparse.ArgumentParser(description='Assign graders to student submissions')
    parser.add_argument('--students', default='students.csv', help='Students CSV file')
    parser.add_argument('--submitted', default='submitted.json', help='Submitted student numbers JSON file')
    parser.add_argument('--graders', default='graders.txt', help='Graders list text file')
    parser.add_argument('--output', default='grading_assignments.csv', help='Output CSV file')
    args = parser.parse_args()

    try:
        # read students data
        students = []
        with open(args.students, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                students.append({
                    'student_number': row['student_number'],
                    'student_name': row['student_name']
                })

        # read submitted student numbers
        with open(args.submitted, 'r') as f:
            submitted_numbers = json.load(f)

        # read graders
        with open(args.graders, 'r') as f:
            graders = [line.strip() for line in f.readlines() if line.strip()]

        # Mark submissions
        submitted_students = []
        for student in students:
            student['submitted'] = 'yes' if student['student_number'] in submitted_numbers else 'no'
            if student['submitted'] == 'yes':
                submitted_students.append(student)

        # Randomize student order
        np.random.shuffle(submitted_students)
        
        # Assign graders
        assignments = defaultdict(list)
        for i, student in enumerate(submitted_students):
            grader = graders[i % len(graders)]
            assignments[grader].append(student)
            student['grader'] = grader

        # Add grader assignment to all students
        for student in students:
            if student['submitted'] == 'no':
                student['grader'] = 'N/A'

        # Save results
        df = pd.DataFrame(students)
        df.to_csv(args.output, index=False)
        
        # Print summary
        print(f"✅ Results saved to {args.output}")
        print("\n📊 Assignment Summary:")
        for grader, st in assignments.items():
            print(f"  - {grader}: {len(st)} students")
            
        print(f"\nTotal submissions: {len(submitted_students)}/{len(students)} students")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e.filename} not found")
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format in submitted.json")
    except KeyError as e:
        print(f"❌ Error: Missing column in CSV - {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
