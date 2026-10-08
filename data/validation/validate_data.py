import csv
from pathlib import Path


# Location of our generated raw data
RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "raw"


# Validate student data
def validate_students():
    students_file = RAW_DATA_DIR / "students.csv"

    total_rows = 0
    student_ids = set()
    duplicate_student_ids = []
    missing_student_ids = []

    with students_file.open("r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_rows += 1

            student_id = row["student_id"]

            # Check 1: student_id cannot be empty
            if not student_id:
                missing_student_ids.append(total_rows)

            # Check 2: student_id must be unique
            if student_id in student_ids:
                duplicate_student_ids.append(student_id)
            else:
                student_ids.add(student_id)

    print("STUDENT DATA QUALITY CHECK")
    print("--------------------------")
    print(f"Total student records: {total_rows}")
    print(f"Missing student IDs: {len(missing_student_ids)}")
    print(f"Duplicate student IDs: {len(duplicate_student_ids)}")

    if not missing_student_ids and not duplicate_student_ids:
        print("RESULT: PASSED")
    else:
        print("RESULT: FAILED")


# Validate attendance data
def validate_attendance():
    students_file = RAW_DATA_DIR / "students.csv"
    attendance_dir = RAW_DATA_DIR / "attendance"

    valid_statuses = {
        "PRESENT",
        "ABSENT",
        "TARDY"
    }

    # Load all valid student IDs from students.csv
    valid_student_ids = set()

    with students_file.open("r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            valid_student_ids.add(row["student_id"])

    total_rows = 0
    missing_student_ids = 0
    invalid_statuses = 0
    unknown_student_ids = 0
    duplicate_records = 0

    seen_records = set()

    # Find all daily attendance CSV files
    attendance_files = sorted(
        attendance_dir.glob("attendance_*.csv")
    )

    # Validate each attendance file
    for attendance_file in attendance_files:

        with attendance_file.open("r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                total_rows += 1

                student_id = row["student_id"]
                attendance_date = row["attendance_date"]
                attendance_status = row["attendance_status"]

                # Check 1: student_id cannot be empty
                if not student_id:
                    missing_student_ids += 1

                # Check 2: attendance status must be valid
                if attendance_status not in valid_statuses:
                    invalid_statuses += 1

                # Check 3: student must exist in students.csv
                if student_id not in valid_student_ids:
                    unknown_student_ids += 1

                # Check 4:
                # A student can only have one attendance record per day
                record_key = (
                    student_id,
                    attendance_date
                )

                if record_key in seen_records:
                    duplicate_records += 1
                else:
                    seen_records.add(record_key)

    print("\nATTENDANCE DATA QUALITY CHECK")
    print("-----------------------------")
    print(f"Attendance files: {len(attendance_files)}")
    print(f"Total attendance records: {total_rows}")
    print(f"Missing student IDs: {missing_student_ids}")
    print(f"Invalid attendance statuses: {invalid_statuses}")
    print(f"Unknown student IDs: {unknown_student_ids}")
    print(f"Duplicate attendance records: {duplicate_records}")

    if (
        missing_student_ids == 0
        and invalid_statuses == 0
        and unknown_student_ids == 0
        and duplicate_records == 0
    ):
        print("RESULT: PASSED")
    else:
        print("RESULT: FAILED")


# Run all data quality checks
if __name__ == "__main__":
    validate_students()
    validate_attendance()