"""Study Buddy Matcher - Matching & Search module (CLI demo).

Examples:
  python -m matching.cli search --query python --min-rating 4
  python -m matching.cli search --day Mon --period evening
  python -m matching.cli tutors-for 1        # suggested tutors for student id 1
  python -m matching.cli students-for 1      # suggested students for tutor id 1
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.data import TUTORS, STUDENTS
from matching.search import search_tutors
from matching.matching import suggest_tutors, suggest_students


def fmt_slots(slots):
    return ", ".join(f"{d} {p}" for d, p in sorted(slots))


def show_tutor(t):
    print(f"  [{t.id}] {t.name}  *{t.rating}")
    print(f"       Courses: {', '.join(t.courses)}")
    print(f"       Free: {fmt_slots(t.availability)}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="search and filter tutors")
    s.add_argument("--query", default="")
    s.add_argument("--min-rating", type=float, default=0.0)
    s.add_argument("--day")
    s.add_argument("--period", choices=["morning", "afternoon", "evening"])
    s.add_argument("--style")

    a = sub.add_parser("tutors-for", help="suggest tutors for a student id")
    a.add_argument("student_id", type=int)

    b = sub.add_parser("students-for", help="suggest students for a tutor id")
    b.add_argument("tutor_id", type=int)

    args = p.parse_args()

    if args.cmd == "search":
        res = search_tutors(TUTORS, args.query, args.min_rating,
                            args.day, args.period, args.style)
        print(f"Found {len(res)} tutor(s):")
        for t in res:
            show_tutor(t)

    elif args.cmd == "tutors-for":
        st = next((x for x in STUDENTS if x.id == args.student_id), None)
        if not st:
            return print("Student not found.")
        print(f"Suggested tutors for {st.name}:")
        for t, sc in suggest_tutors(st, TUTORS):
            print(f"  {sc}% match")
            show_tutor(t)

    elif args.cmd == "students-for":
        tu = next((x for x in TUTORS if x.id == args.tutor_id), None)
        if not tu:
            return print("Tutor not found.")
        print(f"Suggested students for {tu.name}:")
        for s_, sc in suggest_students(tu, STUDENTS):
            print(f"  {sc}% match - {s_.name} needs {', '.join(s_.courses_needed)}")
            print(f"       Free: {fmt_slots(s_.availability)}")


if __name__ == "__main__":
    main()
