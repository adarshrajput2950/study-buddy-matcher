"""Story 3: score and suggest matches between students and tutors."""

W_COURSE, W_TIME, W_STYLE, W_RATING = 50, 25, 10, 15


def match_score(student, tutor):
    """Return a 0-100 match percentage. 0 if no shared course."""
    needed = {c.lower() for c in student.courses_needed}
    taught = {c.lower() for c in tutor.courses}
    shared = needed & taught
    if not shared:
        return 0

    score = W_COURSE * len(shared) / len(needed)

    if student.availability:
        overlap = len(student.availability & tutor.availability)
        score += W_TIME * overlap / len(student.availability)

    if student.learning_style and student.learning_style in tutor.learning_styles:
        score += W_STYLE

    score += W_RATING * (tutor.rating / 5.0)
    return round(score)


def suggest_tutors(student, tutors, limit=3):
    """Top tutors for a student: [(tutor, score), ...] best first."""
    scored = [(t, match_score(student, t)) for t in tutors]
    scored = [x for x in scored if x[1] > 0]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]


def suggest_students(tutor, students, limit=3):
    """Top students for a tutor: [(student, score), ...] best first."""
    scored = [(s, match_score(s, tutor)) for s in students]
    scored = [x for x in scored if x[1] > 0]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]
