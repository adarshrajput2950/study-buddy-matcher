"""Person 1: sign-up, login and profile setup."""
import hashlib
import os

from shared.models import Student, Tutor


def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 50_000).hex()


class UserStore:
    """In-memory accounts. Swap for a database in the build phase."""

    def __init__(self):
        self._accounts = {}  # email -> dict(role, salt, hash, profile)
        self._next_id = {"student": 1, "tutor": 1}

    def register(self, role, name, email, password, **profile):
        if role not in ("student", "tutor"):
            raise ValueError("role must be 'student' or 'tutor'")
        if "@" not in email or len(password) < 6:
            raise ValueError("invalid email or password too short")
        email = email.lower()
        if email in self._accounts:
            raise ValueError("email already registered")
        uid = self._next_id[role]
        self._next_id[role] += 1
        if role == "student":
            user = Student(uid, name, profile.get("courses_needed", []),
                           profile.get("availability", set()),
                           profile.get("learning_style", ""))
        else:
            user = Tutor(uid, name, profile.get("courses", []), 0.0,
                         profile.get("availability", set()),
                         profile.get("learning_styles", []))
        salt = os.urandom(16)
        self._accounts[email] = {"role": role, "salt": salt,
                                 "hash": _hash(password, salt), "user": user}
        return user

    def login(self, email, password):
        acc = self._accounts.get(email.lower())
        if not acc or _hash(password, acc["salt"]) != acc["hash"]:
            return None
        return acc["user"]

    def update_profile(self, email, **changes):
        user = self._accounts[email.lower()]["user"]
        for key, value in changes.items():
            if not hasattr(user, key):
                raise AttributeError(f"unknown profile field: {key}")
            setattr(user, key, value)
        return user
