from pathlib import Path

def generate_monthly_report(month, scenario, total_score, category_scores, contributors, mom_changes, evidence_notes, watchlist):
    lines=[f"# AI Infrastructure Risk Monitor — {month}","","## Summary",f"Monthly monitoring output for {month}.","","## Scenario label",scenario,"","## Total risk score",f"{total_score:.2f}","","## Category scores"]
    lines += [f"- {k}: {v:.2f}" for k,v in category_scores.items()]
    lines += ["","## Top risk contributors"] + [f"- {k}: {v:.2f}" for k,v in contributors]
    lines += ["","## Month-over-month changes"] + [f"- {x}" for x in mom_changes]
    lines += ["","## Evidence notes"] + [f"- {x}" for x in evidence_notes]
    lines += ["","## Next-month watchlist"] + [f"- {x}" for x in watchlist]
    lines += ["","## Methodological notes","- Threshold-based indicator scoring with category and scenario rules.","","## Disclaimer","This report is a structured monitoring output, not investment advice. Scores are model-derived indicators based on selected public or manually entered data and should not be treated as objective probabilities."]
    return "\n".join(lines)

def save_report(report_text:str, month:str, reports_dir='reports'):
    p=Path(reports_dir)/f"{month}-ai-bubble-risk-report.md"
    p.write_text(report_text, encoding='utf-8')
    return str(p)
