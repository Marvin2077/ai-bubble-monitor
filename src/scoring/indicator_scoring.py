def _interp(x,a,b,sa,sb):
    if b==a: return sa
    return sa + (x-a)*(sb-sa)/(b-a)

def score_indicator(value: float, thresholds: dict, history: list[float]|None=None):
    d=thresholds['direction']
    if d=='higher_is_riskier':
        lo,md,hi=thresholds['low'],thresholds['medium'],thresholds['high']
        if value<=lo: return 20, 'value <= low threshold'
        if value<=md: return _interp(value,lo,md,20,50), 'between low and medium'
        if value<=hi: return _interp(value,md,hi,50,80), 'between medium and high'
        return min(100,90+(value-hi)/(hi or 1)*10), 'above high threshold'
    if d=='lower_is_riskier':
        lr,md,hr=thresholds['low_risk'],thresholds['medium'],thresholds['high_risk']
        if value>=lr: return 20, '>= low_risk threshold'
        if value>=md: return _interp(value,md,lr,50,20), 'between medium and low_risk'
        if value>=hr: return _interp(value,hr,md,80,50), 'between high_risk and medium'
        return max(0,90-(value-hr)/(abs(hr) or 1)*10), 'below high_risk threshold'
    if d=='lower_after_peak_is_riskier':
        base, reason=score_indicator(value,{**thresholds,'direction':'lower_is_riskier'},history)
        if history and len(history)>=2:
            prev=history[-1]; roll=max(history[-3:])
            if value < prev and value > thresholds['medium'] and roll-prev > 0:
                return min(100, base+15), 'deceleration after peak adjustment'
        return base, 'fallback lower_is_riskier'
    if d=='deviation_is_riskier':
        return min(100, abs(value-thresholds.get('target',0))), 'deviation score'
    return max(0,min(100,value)), 'manual judgment direct score'
