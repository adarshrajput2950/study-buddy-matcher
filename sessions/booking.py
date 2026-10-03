"""Person 3: request, accept/decline, and remind for study sessions."""
from shared.models import Session


class BookingSystem:
    def __init__(self):
        self.sessions = {}
        self._next = 1

    def _busy(self, key, uid, slot):
        return any(getattr(s, key) == uid and s.slot == slot
                   and s.status == "confirmed"
                   for s in self.sessions.values())

    def request_session(self, student, tutor, course, slot):
        if course not in tutor.courses:
            raise ValueError("tutor does not teach that course")
        if slot not in tutor.availability:
            raise ValueError("tutor is not available in that slot")
        if self._busy("tutor_id", tutor.id, slot):
            raise ValueError("tutor already booked in that slot")
        if self._busy("student_id", student.id, slot):
            raise ValueError("you already have a session in that slot")
        s = Session(self._next, student.id, tutor.id, course, slot)
        self.sessions[s.id] = s
        self._next += 1
        return s

    def respond(self, session_id, accept):
        s = self.sessions[session_id]
        if s.status != "pending":
            raise ValueError("session already answered")
        if accept and self._busy("tutor_id", s.tutor_id, s.slot):
            raise ValueError("tutor already booked in that slot")
        s.status = "confirmed" if accept else "declined"
        return s

    def complete(self, session_id):
        s = self.sessions[session_id]
        if s.status != "confirmed":
            raise ValueError("only confirmed sessions can be completed")
        s.status = "completed"
        return s

    def reminders(self, role, user_id):
        """Confirmed upcoming sessions for a student or tutor."""
        key = "student_id" if role == "student" else "tutor_id"
        return [f"Reminder: {s.course} on {s.slot[0]} {s.slot[1]}"
                for s in self.sessions.values()
                if getattr(s, key) == user_id and s.status == "confirmed"]
