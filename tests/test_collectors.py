from src.collectors.fred_collector import collect_fred_latest_observation
from src.collectors.manual_stub_collector import collect_manual_registry


class DummyResp:
    def __init__(self, text: str):
        self._text = text.encode('utf-8')

    def read(self):
        return self._text

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_fred_collector_parses_latest(monkeypatch):
    csv_text = "DATE,BAMLH0A0HYM2\n2026-03-01,350\n2026-04-01,360\n"
    monkeypatch.setattr('urllib.request.urlopen', lambda *args, **kwargs: DummyResp(csv_text))
    obs = collect_fred_latest_observation('US_HIGH_YIELD_SPREAD', 'BAMLH0A0HYM2')
    assert obs is not None
    assert obs.date == '2026-04'
    assert obs.value == 360.0


def test_manual_registry_collector_reads_rows(tmp_path):
    p = tmp_path / 'm.csv'
    p.write_text('date,indicator_id,value,source_url,notes,confidence,input_type\n2026-04,NASDAQ_DRAWDOWN,8,u,n,0.7,observed\n', encoding='utf-8')
    rows = collect_manual_registry(str(p))
    assert len(rows) == 1
    assert rows[0].indicator_id == 'NASDAQ_DRAWDOWN'
