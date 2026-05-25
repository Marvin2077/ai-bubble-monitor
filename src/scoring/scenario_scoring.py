from src.models import ScenarioResult

def select_scenario(date:str,total_score:float,category_scores:dict)->ScenarioResult:
    s0=100 if (total_score<35 and category_scores.get('gpu_cycle',0)<45 and category_scores.get('ai_cloud_financing',0)<45) else 0
    s1=100 if (35<=total_score<60 and max(category_scores.values() or [0])<75) else 0
    s2=100 if ((60<=total_score<75) or category_scores.get('ai_cloud_financing',0)>=75 or (category_scores.get('compute_price_pressure',0)>=75 and category_scores.get('gpu_cycle',0)>=60)) else 0
    flags=sum([category_scores.get('ai_cloud_financing',0)>=75,category_scores.get('macro_credit',0)>=75,category_scores.get('hyperscaler_capex',0)>=70,category_scores.get('gpu_cycle',0)>=70])
    s3=100 if (total_score>=75 and flags>=2) else 0
    final='S0'
    for s,v in [('S1',s1),('S2',s2),('S3',s3)]:
        if v>0: final=s
    return ScenarioResult(date=date,total_score=total_score,s0_score=s0,s1_score=s1,s2_score=s2,s3_score=s3,final_label=final,explanation='Rule-based regime label, not probability.')
