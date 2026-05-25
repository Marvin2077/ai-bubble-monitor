def top_contributors(indicator_scores: dict, n:int=5):
    return sorted(indicator_scores.items(), key=lambda x:x[1], reverse=True)[:n]
