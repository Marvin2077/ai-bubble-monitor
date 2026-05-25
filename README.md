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

## Monthly workflow (recommended)
1. Click **Import sample CSV** (or import your own monthly CSV).
2. Optionally click **Auto-collect public data (optional)** for selected public sources (FRED/SEC/manual registry).
3. Review evidence notes and confidence.
4. Check total score + scenario label.
5. Generate monthly markdown report.

## Import monthly CSV data
Required columns:
`date, indicator_id, value, source_url, notes, confidence, input_type`.

## Automatic data collection scope (MVP)
- Supports optional public-source collection:
  - FRED series (macro indicators)
  - SEC CompanyFacts (company financial fields)
  - local manual evidence registry (`data/manual_evidence_registry.csv`)
- If network/source fails, collector returns empty and dashboard still works.
- CSV/manual input remains primary fallback.

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
- Public auto-collection is partial and best-effort; analyst review is required.
- Some indicators (e.g., China substitution scores) remain judgment-heavy and should be manually maintained.

## Disclaimer
This report is a structured monitoring output, not investment advice. Scores are model-derived indicators based on selected public or manually entered data and should not be treated as objective probabilities.
