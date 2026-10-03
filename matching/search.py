"""Story 1 and 2: search tutors by course, then filter by rating/availability."""


def search_tutors(tutors, query="", min_rating=0.0, day=None,
                  period=None, style=None):
    """Return tutors matching all given filters, best rated first.

    query   - partial course name or tutor name (case-insensitive)
    day     - e.g. "Mon"; period - "morning" / "afternoon" / "evening"
    style   - learning style the tutor supports, e.g. "visual"
    """
    q = query.strip().lower()
    results = []
    for t in tutors:
        if q and not (q in t.name.lower()
                      or any(q in c.lower() for c in t.courses)):
            continue
        if t.rating < min_rating:
            continue
        if day and not any(d == day for d, _ in t.availability):
            continue
        if period and not any(p == period for _, p in t.availability):
            continue
        if day and period and (day, period) not in t.availability:
            continue
        if style and style not in t.learning_styles:
            continue
        results.append(t)
    return sorted(results, key=lambda t: t.rating, reverse=True)
