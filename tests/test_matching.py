import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.data import TUTORS, STUDENTS
from matching.search import search_tutors
from matching.matching import match_score, suggest_tutors, suggest_students


class TestSearch(unittest.TestCase):
    def test_search_by_course(self):
        names = [t.name for t in search_tutors(TUTORS, "python")]
        self.assertIn("Neha Gupta", names)
        self.assertNotIn("Karan Singh", names)

    def test_min_rating(self):
        self.assertTrue(all(t.rating >= 4.5
                            for t in search_tutors(TUTORS, min_rating=4.5)))

    def test_day_and_period(self):
        res = search_tutors(TUTORS, day="Wed", period="evening")
        self.assertEqual({t.name for t in res}, {"Aman Verma", "Priya Thakur"})

    def test_sorted_by_rating(self):
        r = [t.rating for t in search_tutors(TUTORS)]
        self.assertEqual(r, sorted(r, reverse=True))


class TestMatching(unittest.TestCase):
    def test_no_shared_course_is_zero(self):
        riya, karan = STUDENTS[0], TUTORS[2]
        self.assertEqual(match_score(riya, karan), 0)

    def test_best_tutor_for_riya(self):
        best, score = suggest_tutors(STUDENTS[0], TUTORS)[0]
        self.assertEqual(best.name, "Aman Verma")
        self.assertGreater(score, 80)

    def test_students_for_tutor(self):
        res = suggest_students(TUTORS[4], STUDENTS)  # Rohit: Python, Algorithms
        self.assertEqual(res[0][0].name, "Arjun Mehta")

    def test_score_in_range(self):
        for s in STUDENTS:
            for t in TUTORS:
                self.assertTrue(0 <= match_score(s, t) <= 100)


if __name__ == "__main__":
    unittest.main()
