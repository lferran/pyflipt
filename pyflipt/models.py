from pydantic import BaseModel
from typing import Optional, Dict
from enum import Enum


class FliptBasicUnit(BaseModel):
    ...


class Flag(FliptBasicUnit):
    key: str
    name: str
    description: Optional[str]
    enabled: bool


class Rule(FliptBasicUnit):
    flag_key: str
    segment_key: str
    rank: int


class MatchType(Enum):
    ALL = "ALL_MATCH_TYPE"
    ANY = "ANY_MATCH_TYPE"


class Segment(FliptBasicUnit):
    key: str
    name: str
    description: Optional[str]
    match_type: MatchType = MatchType.ALL.value


class ComparisonType(Enum):
    UNKNOWN = "UNKNOWN_COMPARISON_TYPE"
    STRING = "STRING_COMPARISON_TYPE"
    NUMBER = "NUMBER_COMPARISON_TYPE"
    BOOLEAN = "BOOLEAN_COMPARISON_TYPE"


class Constraint(FliptBasicUnit):
    segment_key: str
    type: ComparisonType = ComparisonType.UNKNOWN.value
    property: str
    operator: str
    value: str


class EvaluateResponse(BaseModel):
    request_context: Dict[str, str]
    match: bool
    flag_key: str
    segment_key: str
    value: str
