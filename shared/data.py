from shared.models import Tutor, Student

TUTORS = [
    Tutor(1, "Aman Verma", ["Data Structures", "Algorithms"], 4.8,
          {("Mon", "evening"), ("Wed", "evening"), ("Sat", "morning")},
          ["visual", "practice"]),
    Tutor(2, "Neha Gupta", ["Python", "Data Structures"], 4.5,
          {("Tue", "afternoon"), ("Thu", "evening"), ("Sat", "morning")},
          ["practice"]),
    Tutor(3, "Karan Singh", ["Calculus", "Linear Algebra"], 4.2,
          {("Mon", "morning"), ("Fri", "evening")},
          ["reading", "visual"]),
    Tutor(4, "Priya Thakur", ["DBMS", "Operating Systems"], 4.9,
          {("Wed", "evening"), ("Sun", "afternoon")},
          ["discussion"]),
    Tutor(5, "Rohit Sharma", ["Python", "Algorithms"], 3.9,
          {("Mon", "evening"), ("Tue", "evening")},
          ["practice", "discussion"]),
]

STUDENTS = [
    Student(1, "Riya Sharma", ["Data Structures"],
            {("Mon", "evening"), ("Sat", "morning")}, "visual"),
    Student(2, "Arjun Mehta", ["Python", "Algorithms"],
            {("Tue", "evening"), ("Mon", "evening")}, "practice"),
    Student(3, "Simran Kaur", ["DBMS"],
            {("Wed", "evening")}, "discussion"),
]
