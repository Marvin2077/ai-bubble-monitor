from src.reporting.markdown_report import generate_monthly_report

def test_monthly_report_generation():
    t=generate_monthly_report('2026-03','S1',50,{'gpu_cycle':50},[('x',70)],[],[],[])
    assert 'Disclaimer' in t and 'not investment advice' in t
