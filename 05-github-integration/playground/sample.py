"""Auto-review target.

Open a PR that edits this file and the `Claude auto review` workflow will
review the change. The functions below contain deliberate issues so the
review has something to catch. Try fixing one (or adding a new flaw) in a PR.
"""


def average(numbers):
    # Deliberate bug: no guard for an empty list (ZeroDivisionError).
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)


def get_user(db, user_id):
    # Deliberate bug: SQL injection via string interpolation.
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)


def ping(host, count=1):
    # New in this PR: ping a host `count` times and return the raw output.
    # Deliberate bug: command injection (unsanitized input into a shell).
    import os

    return os.popen("ping -c " + str(count) + " " + host).read()
