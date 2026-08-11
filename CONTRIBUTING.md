# Contributing

Contributions are welcome when they improve accountability, interoperability, validation, or documentation.

1. Open an issue describing the real workflow problem.
2. Keep examples fictional and free of customer or personal data.
3. Add or update tests when changing validation behavior.
4. Run `python3 scripts/validate_artifacts.py` and `python3 -m unittest discover -s tests -v`.
5. Submit a focused pull request.

Role definitions should describe an accountable outcome, allowed actions, prohibited actions, required inputs, and verifiable outputs. Avoid adding a role only because a prompt sounds useful.
