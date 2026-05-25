from src.scoring.indicator_scoring import score_indicator

def test_higher_is_riskier():
    s,_=score_indicator(90, {'direction':'higher_is_riskier','low':30,'medium':60,'high':80})
    assert s>=90

def test_lower_is_riskier():
    s,_=score_indicator(30, {'direction':'lower_is_riskier','low_risk':80,'medium':60,'high_risk':40})
    assert s>=80

def test_lower_after_peak_is_riskier():
    s,_=score_indicator(55, {'direction':'lower_after_peak_is_riskier','low_risk':80,'medium':50,'high_risk':30}, history=[90,80,70])
    assert s>=20
