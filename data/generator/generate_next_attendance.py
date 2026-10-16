import csv
import random
from pathlib import Path

random.seed(43)

RAW_DIR = Path(__file__).resolve().parent.parent / "raw"
STUDENTS_FILE = RAW_DIR / "students.csv"
OUTPUT_FILE = RAW_DIR / "attendance" / "attendance_2026-09-24.csv"

with STUDENTS_FILE.open("r", newline="") as file:
    reader = csv.DictReader(file)
    student_ids = [row["student_id"] for row in reader]

with OUTPUT_FILE.open("w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "student_id",
        "attendance_date",
        "attendance_status"
    ])

    for student_id in student_ids:
        status = random.choices(
            ["PRESENT", "ABSENT", "TARDY"],
            weights=[94, 4, 2],
            k=1
        )[0]


        writer.writerow([
            student_id,
            "2026-09-24",
            status
        ])

print(f"Created: {OUTPUT_FILE}")
print(f"Records: {len(student_ids)}")