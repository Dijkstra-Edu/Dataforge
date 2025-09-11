from Schema.SQL.Enums.enums import Tools
from Utils.Exceptions.opportunities_exceptions import InvalidTools

def _validate_tools(values, field_name: str):
    if values:
        invalid = [v for v in values if v not in Tools._value2member_map_]
        if invalid:
            raise InvalidTools(invalid, field_name, list(Tools))
