import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Makes our synthetic dataset reproducible.
random.seed(42)

# Folder where generated CSV files will be stored.
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Project configuration
NUM_STUDENTS = 10_000
SCHOOL_START_DATE = date(2026, 8, 10)
NUM_SCHOOL_DAYS = 30


# Synthetic campus master data
CAMPUSES = [
    ("CAMP001", "Victory Academy", "Tampa Bay", "FL"),
    ("CAMP002", "Hope Academy", "Tampa Bay", "FL"),
    ("CAMP003", "Lakeland Academy", "Tampa Bay", "FL"),
    ("CAMP004", "Bassett Academy", "Jacksonville", "FL"),
    ("CAMP005", "Compass Academy", "Jacksonville", "FL"),
    ("CAMP006", "River Bluff Academy", "Jacksonville", "FL"),
    ("CAMP007", "Rio Grande Academy", "Rio Grande Valley", "TX"),
    ("CAMP008", "Frontier Academy", "San Antonio", "TX"),
    ("CAMP009", "Innovation Academy", "Austin", "TX"),
    ("CAMP010", "North Mission Academy", "Rio Grande Valley", "TX"),
]


# Generate a random date between two dates
def random_date(start_date, end_date):
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)

    return start_date + timedelta(days=random_days)


# Generate campus master data
def generate_campuses():
    output_file = OUTPUT_DIR / "campuses.csv"

    with output_file.open("w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "campus_id",
            "campus_name",
            "region",
            "state"
        ])

        writer.writerows(CAMPUSES)

    print(f"Created: {output_file}")


# Generate synthetic student data
def generate_students():
    output_file = OUTPUT_DIR / "students.csv"

    with output_file.open("w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "student_id",
            "campus_id",
            "grade_level",
            "enrollment_date",
            "student_status"
        ])

        for i in range(1, NUM_STUDENTS + 1):

            student_id = f"STU{i:06d}"

            campus_id = random.choice(CAMPUSES)[0]

            grade_level = random.randint(0, 12)

            enrollment_date = random_date(
                date(2022, 8, 1),
                date(2026, 8, 15)
            )

            student_status = random.choices(
                ["ACTIVE", "WITHDRAWN"],
                weights=[95, 5],
                k=1
            )[0]

            writer.writerow([
                student_id,
                campus_id,
                grade_level,
                enrollment_date.isoformat(),
                student_status
            ])

    print(f"Created: {output_file}")


# Generate school days and skip weekends
def get_school_days(start_date, number_of_days):

    school_days = []
    current_date = start_date

    while len(school_days) < number_of_days:

        # Monday = 0
        # Friday = 4
        # Saturday = 5
        # Sunday = 6

        if current_date.weekday() < 5:
            school_days.append(current_date)

        current_date += timedelta(days=1)

    return school_days


# Generate daily attendance files
def generate_attendance():

    attendance_dir = OUTPUT_DIR / "attendance"

    attendance_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    school_days = get_school_days(
        SCHOOL_START_DATE,
        NUM_SCHOOL_DAYS
    )

    for school_day in school_days:

        output_file = (
            attendance_dir
            / f"attendance_{school_day}.csv"
        )

        with output_file.open("w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "student_id",
                "attendance_date",
                "attendance_status"
            ])

            for i in range(1, NUM_STUDENTS + 1):

                student_id = f"STU{i:06d}"

                attendance_status = random.choices(
                    [
                        "PRESENT",
                        "ABSENT",
                        "TARDY"
                    ],
                    weights=[
                        94,
                        4,
                        2
                    ],
                    k=1
                )[0]

                writer.writerow([
                    student_id,
                    school_day.isoformat(),
                    attendance_status
                ])

        print(f"Created: {output_file}")


# Run the data generator
if __name__ == "__main__":

    generate_campuses()

    generate_students()

    generate_attendance()

    print("\nSynthetic K-12 data generation completed.")