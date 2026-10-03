"""Person 4: per-session chat and post-session ratings."""
from shared.models import Review


class ChatBoard:
    def __init__(self):
        self._messages = {}  # session_id -> [(sender, text)]

    def send(self, session, sender, text):
        if session.status not in ("confirmed", "completed"):
            raise ValueError("chat opens once a session is confirmed")
        if not text.strip():
            raise ValueError("empty message")
        self._messages.setdefault(session.id, []).append((sender, text.strip()))

    def history(self, session):
        return list(self._messages.get(session.id, []))


class ReviewBoard:
    def __init__(self):
        self._reviews = {}  # session_id -> Review
        self._by_tutor = {}  # tutor_id -> [stars]

    def add_review(self, session, tutor, stars, comment=""):
        if session.status != "completed":
            raise ValueError("you can only rate completed sessions")
        if not 1 <= stars <= 5:
            raise ValueError("stars must be 1-5")
        if session.id in self._reviews:
            raise ValueError("session already reviewed")
        self._reviews[session.id] = Review(session.id, stars, comment)
        self._by_tutor.setdefault(tutor.id, []).append(stars)
        tutor.rating = self.average(tutor.id)  # shows on profile and search
        return self._reviews[session.id]

    def average(self, tutor_id):
        r = self._by_tutor.get(tutor_id, [])
        return round(sum(r) / len(r), 1) if r else 0.0
