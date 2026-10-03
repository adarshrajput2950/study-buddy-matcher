"""Study Buddy Matcher - end-to-end demo joining all 4 modules.

Run:  python app.py
Matching CLI:  python -m matching.cli search --query python
"""
from onboarding.profile import UserStore
from matching.search import search_tutors
from matching.matching import suggest_tutors
from sessions.booking import BookingSystem
from chat_ratings.chat import ChatBoard, ReviewBoard


def demo():
    users, booking, chat, reviews = UserStore(), BookingSystem(), ChatBoard(), ReviewBoard()

    # Person 1: onboarding
    tutor = users.register("tutor", "Aman Verma", "aman@uni.edu", "secret123",
                           courses=["Data Structures"], learning_styles=["visual"],
                           availability={("Mon", "evening"), ("Sat", "morning")})
    riya = users.register("student", "Riya Sharma", "riya@uni.edu", "secret123",
                          courses_needed=["Data Structures"], learning_style="visual",
                          availability={("Mon", "evening")})
    assert users.login("riya@uni.edu", "secret123") is riya
    print(f"1. Registered {tutor.name} (tutor) and {riya.name} (student)")

    # Person 2: search and matching
    found = search_tutors([tutor], "data structures")
    best, score = suggest_tutors(riya, [tutor])[0]
    print(f"2. Search found {len(found)} tutor; best match {best.name} ({score}%)")

    # Person 3: booking
    s = booking.request_session(riya, tutor, "Data Structures", ("Mon", "evening"))
    booking.respond(s.id, accept=True)
    print(f"3. Session {s.id} {s.status}; {booking.reminders('student', riya.id)[0]}")

    # Person 4: chat and ratings
    chat.send(s, riya.name, "Hi! Can we start with trees?")
    chat.send(s, tutor.name, "Sure, bring your questions.")
    booking.complete(s.id)
    reviews.add_review(s, tutor, 5, "Very clear explanations")
    print(f"4. Chat messages: {len(chat.history(s))}; "
          f"{tutor.name}'s rating is now {tutor.rating}")


if __name__ == "__main__":
    demo()
