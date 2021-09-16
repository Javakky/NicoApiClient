from datetime import datetime
from typing import Dict, List, Optional, Union


class ComplexFilterTerm:
    def __init__(self):
        self.json: Dict[str, Union[str, bool, int]] = {}


def set_range_view(
        start: Optional[int] = None,
        end: Optional[int] = None,
        include_lower: bool = True,
        include_upper: bool = True,
) -> 'ComplexFilterTerm':
    term: ComplexFilterTerm = ComplexFilterTerm()
    if start is None and end is None:
        raise Exception("上限も下限も指定されていません")
    json_: Dict[str, Union[str, bool, int]] = {
        "type": "range",
        "field": "viewCounter"
    }
    if start is not None:
        json_["from"] = start
    if end is not None:
        json_["to"] = end
    if include_lower:
        json_["include_lower"] = include_lower
    if include_upper:
        json_["include_upper"] = include_upper
    term.json = json_
    return term


def set_range_time(
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        include_lower: bool = True,
        include_upper: bool = True,
) -> 'ComplexFilterTerm':
    term: ComplexFilterTerm = ComplexFilterTerm()
    if start is None and end is None:
        raise Exception("開始時刻も終了時刻も指定されていません")
    json_: Dict[str, Union[str, bool]] = {
        "type": "range",
        "field": "startTime"
    }
    if start is not None:
        json_["from"] = start.strftime('%Y-%m-%dT%H:%M:%S+09:00')
    if end is not None:
        json_["to"] = end.strftime('%Y-%m-%dT%H:%M:%S+09:00')
    if include_lower:
        json_["include_lower"] = include_lower
    if include_upper:
        json_["include_upper"] = include_upper
    term.json = json_
    return term


TypeOp = Dict[str, Union[str, bool, int, List['TypeOp'], 'TypeOp']]


class ComplexFilterOperator:
    def __init__(self, json_: TypeOp):
        self.json: TypeOp = json_


def unit(term: 'ComplexFilterTerm') -> 'ComplexFilterOperator':
    return ComplexFilterOperator(term.json)


def not_(
        term: Union['ComplexFilterTerm', 'ComplexFilterOperator']
):
    json_: TypeOp = {
        "type": "not",
        "filter": term.json
    }
    return ComplexFilterOperator(json_)


def binary(
        op_name: str,
        left: Union['ComplexFilterTerm', 'ComplexFilterOperator'],
        right: Union['ComplexFilterTerm', 'ComplexFilterOperator']
):
    json_: TypeOp = {
        "type": op_name,
        "filters": []
    }
    json_["filters"].append(left.json)
    json_["filters"].append(right.json)
    return ComplexFilterOperator(json_)


def or_(
        left: Union['ComplexFilterTerm', 'ComplexFilterOperator'],
        right: Union['ComplexFilterTerm', 'ComplexFilterOperator']
) -> 'ComplexFilterOperator':
    return binary("or", left, right)


def and_(
        left: Union['ComplexFilterTerm', 'ComplexFilterOperator'],
        right: Union['ComplexFilterTerm', 'ComplexFilterOperator']
) -> 'ComplexFilterOperator':
    return binary("and", left, right)
