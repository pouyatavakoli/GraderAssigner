#!/usr/bin/env python3

import json
import csv
import numpy as np
import pandas as pd
from collections import defaultdict
import argparse

def prompt_continue():
    while True:
        response = input("\n⚠️  Missing submissions detected. Continue anyway? (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        print("Please enter 'y' or 'n'.")

def main():
    # command-line arguments
    parser = argparse.ArgumentParser(description='Assign graders to student submissions')
    parser.add_argument('--students', default='students.csv', help='Students CSV file')
    parser.add_argument('--submitted', default='submitted.json', help='Submitted student numbers JSON file')
    parser.add_argument('--graders', default='graders.txt', help='Graders list text file')
    parser.add_argument('--output', default='grading_assignments.csv', help='Output CSV file')
    parser.add_argument('--check-missing', action='store_true', 
                        help='Check for submissions that are not in students file')
    args = parser.parse_args()

    try:
        # read students data
        students = []
        student_numbers = set()
        with open(args.students, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                students.append({
                    'student_number': row['student_number'],
                    'student_name': row['student_name']
                })
                student_numbers.add(row['student_number'])

        # read submitted student numbers
        with open(args.submitted, 'r') as f:
            submitted_numbers = json.load(f)

        # If check-missing flag is set, find submissions not in students file
        if args.check_missing:
            missing_submissions = [num for num in submitted_numbers if num not in student_numbers]
            if missing_submissions:
                print("\n⚠️  The following submissions were not found in the students file:")
                for num in missing_submissions:
                    print(f"  - {num}")
                print(f"\nTotal missing submissions: {len(missing_submissions)}")

                # prompt user if they want to continue 
                if not prompt_continue():
                    print("Exiting...")
                    return
            else:
                print("\n✅ All submissions match students in the students file\n generating the grading list...")
    
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

        # Add footer
        with open(args.output, 'a') as f:

            f.write('\n')  # Empty line separator
            f.write('Generated with ❤️ using GraderAssigner\n')
            f.write('https://github.com/pouyatavakoli/GraderAssigner\n')
        
        
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
