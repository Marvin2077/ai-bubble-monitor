from src.scoring.scenario_scoring import select_scenario

def test_scenario_selection():
    r=select_scenario('2026-03',78,{'ai_cloud_financing':80,'macro_credit':76,'hyperscaler_capex':60,'gpu_cycle':71})
    assert r.final_label=='S3'
