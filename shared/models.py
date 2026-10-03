from dataclasses import dataclass, field

# A slot is a (day, period) pair, e.g. ("Mon", "evening")
Slot = tuple


@dataclass
class Tutor:
    id: int
    name: str
    courses: list
    rating: float
    availability: set = field(default_factory=set)
    learning_styles: list = field(default_factory=list)


@dataclass
class Student:
    id: int
    name: str
    courses_needed: list
    availability: set = field(default_factory=set)
    learning_style: str = ""


@dataclass
class Session:
    id: int
    student_id: int
    tutor_id: int
    course: str
    slot: tuple  # (day, period)
    status: str = "pending"  # pending / confirmed / declined / completed


@dataclass
class Review:
    session_id: int
    stars: int
    comment: str = ""
