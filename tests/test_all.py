import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from onboarding.profile import UserStore
from sessions.booking import BookingSystem
from chat_ratings.chat import ChatBoard, ReviewBoard
from shared.models import Student, Tutor

SLOT = ("Mon", "evening")


def make():
    t = Tutor(1, "T", ["Python"], 0.0, {SLOT})
    s = Student(1, "S", ["Python"], {SLOT})
    return s, t


class TestOnboarding(unittest.TestCase):
    def test_register_login(self):
        u = UserStore()
        user = u.register("student", "A", "a@x.com", "pass123")
        self.assertIs(u.login("A@x.com", "pass123"), user)
        self.assertIsNone(u.login("a@x.com", "wrong"))

    def test_duplicate_and_weak(self):
        u = UserStore()
        u.register("tutor", "A", "a@x.com", "pass123")
        with self.assertRaises(ValueError):
            u.register("tutor", "B", "a@x.com", "pass123")
        with self.assertRaises(ValueError):
            u.register("tutor", "B", "b@x.com", "123")

    def test_update_profile(self):
        u = UserStore()
        u.register("student", "A", "a@x.com", "pass123")
        self.assertEqual(u.update_profile("a@x.com", learning_style="visual").learning_style, "visual")


class TestBooking(unittest.TestCase):
    def test_flow_and_reminder(self):
        s, t = make()
        b = BookingSystem()
        sess = b.request_session(s, t, "Python", SLOT)
        b.respond(sess.id, True)
        self.assertEqual(len(b.reminders("student", s.id)), 1)

    def test_rejects_bad_requests(self):
        s, t = make()
        b = BookingSystem()
        with self.assertRaises(ValueError):
            b.request_session(s, t, "Calculus", SLOT)
        with self.assertRaises(ValueError):
            b.request_session(s, t, "Python", ("Tue", "morning"))

    def test_double_booking_blocked(self):
        s, t = make()
        s2 = Student(2, "S2", ["Python"], {SLOT})
        b = BookingSystem()
        b.respond(b.request_session(s, t, "Python", SLOT).id, True)
        with self.assertRaises(ValueError):
            b.request_session(s2, t, "Python", SLOT)

    def test_decline(self):
        s, t = make()
        b = BookingSystem()
        sess = b.request_session(s, t, "Python", SLOT)
        self.assertEqual(b.respond(sess.id, False).status, "declined")


class TestChatRatings(unittest.TestCase):
    def setUp(self):
        self.s, self.t = make()
        self.b = BookingSystem()
        self.sess = self.b.request_session(self.s, self.t, "Python", SLOT)

    def test_chat_needs_confirmation(self):
        with self.assertRaises(ValueError):
            ChatBoard().send(self.sess, "S", "hi")
        self.b.respond(self.sess.id, True)
        c = ChatBoard()
        c.send(self.sess, "S", " hi ")
        self.assertEqual(c.history(self.sess), [("S", "hi")])

    def test_rating_rules(self):
        r = ReviewBoard()
        self.b.respond(self.sess.id, True)
        with self.assertRaises(ValueError):
            r.add_review(self.sess, self.t, 5)  # not completed yet
        self.b.complete(self.sess.id)
        with self.assertRaises(ValueError):
            r.add_review(self.sess, self.t, 6)
        r.add_review(self.sess, self.t, 4)
        self.assertEqual(self.t.rating, 4.0)
        with self.assertRaises(ValueError):
            r.add_review(self.sess, self.t, 5)  # duplicate


if __name__ == "__main__":
    unittest.main()
