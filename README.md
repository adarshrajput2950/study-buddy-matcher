# Study Buddy Matcher (all 4 modules)

Pure Python 3, no installs.

    python app.py                                   # end-to-end demo
    python -m matching.cli search --query python    # Person 2 CLI
    python -m unittest discover -s tests -v         # run tests

| Folder        | Owner    | What it does                              |
|---------------|----------|-------------------------------------------|
| onboarding/   | Person 1 | sign-up, login (hashed passwords), profile |
| matching/     | Person 2 | search, filters, match score, suggestions |
| sessions/     | Person 3 | request, accept/decline, reminders        |
| chat_ratings/ | Person 4 | session chat, ratings and reviews         |
| shared/       | everyone | models and sample data                    |
