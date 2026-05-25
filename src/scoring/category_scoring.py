def score_category(indicator_scores, indicators):
    total=0; wsum=0
    for iid,score in indicator_scores.items():
        w=indicators[iid]['weight']
        total += score*w; wsum += w
    return (total/wsum if wsum else 0), 'weighted average'
