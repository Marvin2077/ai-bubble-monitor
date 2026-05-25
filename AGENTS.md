# AGENTS Rules

- Keep the project local-first.
- Do not hard-code indicator definitions or thresholds inside Python files.
- Use YAML config files for indicators, thresholds, category weights, and scenario rules.
- Every score must be traceable to observations.
- Never present scenario labels as objective probabilities.
- Prefer simple, testable functions over complex abstractions.
- Add or update tests whenever scoring logic changes.
- Use type hints for all public functions.
- Use docstrings for scoring functions.
- Keep external data collectors isolated under src/collectors/.
- If a data source is unstable, support manual override.
- Keep UI code separate from scoring logic.
- Tests must run with pytest.
