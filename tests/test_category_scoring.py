from src.scoring.category_scoring import score_category

def test_category_weighted_average():
    score,_=score_category({'a':80,'b':20},{'a':{'weight':0.75},'b':{'weight':0.25}})
    assert round(score,2)==65
