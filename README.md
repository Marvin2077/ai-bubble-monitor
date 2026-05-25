# AI Bubble Monitor

Local-first monthly risk monitoring dashboard for AI infrastructure cycle risk regimes (S0-S3). This is not a crash predictor.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```
Windows:
```bat
.venv\Scripts\activate
```

## Run app
```bash
streamlit run app.py
```

## Import monthly CSV data
Use the `Import sample CSV` button or call importer in code with required columns:
`date, indicator_id, value, source_url, notes, confidence, input_type`.

## Scoring methodology
- Indicator score: threshold-based and direction-specific.
- Category score: weighted average of indicator scores.
- Scenario label: rules over total score and categories.
- Scenario labels are regime labels, not probabilities.

## Add new indicator
1. Add indicator in `configs/indicators.yaml`.
2. Add threshold in `configs/thresholds.yaml`.
3. Ensure category weight exists.

## Edit thresholds
Update `configs/thresholds.yaml` and rerun scoring.

## Generate monthly report
Use "Generate report" button in app. Output saved to `reports/YYYY-MM-ai-bubble-risk-report.md`.

## Tests
```bash
pytest
```

## Limitations
- MVP-1 focuses on CSV/manual inputs.
- Collectors are stubs and optional.

## Disclaimer
This report is a structured monitoring output, not investment advice. Scores are model-derived indicators based on selected public or manually entered data and should not be treated as objective probabilities.
