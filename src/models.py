from dataclasses import dataclass
from typing import Optional
import re

DATE_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")

def _check_date(v: str):
    if not DATE_RE.match(v):
        raise ValueError('date must be YYYY-MM')

@dataclass
class Indicator:
    id: str; name: str; category: str; unit: str; source_type: str; source_url: Optional[str]; direction: str; weight: float; description: str; manual_required: bool

@dataclass
class Observation:
    indicator_id: str; date: str; value: float; confidence: float; input_type: str; id: Optional[int]=None; raw_value: Optional[str]=None; source_url: Optional[str]=None; notes: Optional[str]=None
    def __post_init__(self):
        _check_date(self.date)
        if not (0 <= float(self.confidence) <= 1): raise ValueError('confidence must be 0..1')
        if self.input_type not in {'observed','manual','derived'}: raise ValueError('invalid input_type')

@dataclass
class IndicatorScore:
    indicator_id: str; date: str; score: float; reason: str

@dataclass
class CategoryScore:
    category: str; date: str; score: float; reason: str

@dataclass
class ScenarioResult:
    date: str; total_score: float; s0_score: float; s1_score: float; s2_score: float; s3_score: float; final_label: str; explanation: str
