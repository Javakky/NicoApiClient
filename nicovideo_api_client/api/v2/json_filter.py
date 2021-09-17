from datetime import datetime
from typing import Dict, List, Optional, Union


class JsonFilterTerm:
    def __init__(self):
        self.json: Dict[str, Union[str, bool, int]] = {}

    @staticmethod
    def set_range_view(
            start: Optional[int] = None,
            end: Optional[int] = None,
            include_lower: bool = True,
            include_upper: bool = True,
    ) -> 'JsonFilterTerm':
        term: JsonFilterTerm = JsonFilterTerm()
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

    @staticmethod
    def set_range_time(
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            include_lower: bool = True,
            include_upper: bool = True,
    ) -> 'JsonFilterTerm':
        term: JsonFilterTerm = JsonFilterTerm()
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


class JsonFilterOperator:
    def __init__(self, json_: TypeOp):
        self.json: TypeOp = json_

    @staticmethod
    def unit(term: 'JsonFilterTerm') -> 'JsonFilterOperator':
        return JsonFilterOperator(term.json)

    @staticmethod
    def not_(
            term: Union['JsonFilterTerm', 'JsonFilterOperator']
    ):
        json_: TypeOp = {
            "type": "not",
            "filter": term.json
        }
        return JsonFilterOperator(json_)

    @staticmethod
    def _binary(
            op_name: str,
            left: Union['JsonFilterTerm', 'JsonFilterOperator'],
            right: Union['JsonFilterTerm', 'JsonFilterOperator']
    ):
        json_: TypeOp = {
            "type": op_name,
            "filters": []
        }
        json_["filters"].append(left.json)
        json_["filters"].append(right.json)
        return JsonFilterOperator(json_)

    @staticmethod
    def or_(
            left: Union['JsonFilterTerm', 'JsonFilterOperator'],
            right: Union['JsonFilterTerm', 'JsonFilterOperator']
    ) -> 'JsonFilterOperator':
        return JsonFilterOperator._binary("or", left, right)

    @staticmethod
    def and_(
            left: Union['JsonFilterTerm', 'JsonFilterOperator'],
            right: Union['JsonFilterTerm', 'JsonFilterOperator']
    ) -> 'JsonFilterOperator':
        return JsonFilterOperator._binary("and", left, right)
