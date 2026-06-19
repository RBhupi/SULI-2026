from dataclasses import dataclass


@dataclass
class FilterCondition:
    field: str
    operator: str
    value1: str = ""
    value2: str = ""
    logical_op: str = "AND"


OPERATORS = [
    "=", "!=", ">", "<", ">=", "<=",
    "Contains", "Starts With", "Ends With",
    "Between", "Is Null", "Not Null"
]


def build_condition(c):
    f = f'"{c.field}"'

    if c.operator == "=":
        return f"{f} = ?", [c.value1]
    if c.operator == "!=":
        return f"{f} != ?", [c.value1]
    if c.operator == ">":
        return f"{f} > ?", [c.value1]
    if c.operator == "<":
        return f"{f} < ?", [c.value1]
    if c.operator == ">=":
        return f"{f} >= ?", [c.value1]
    if c.operator == "<=":
        return f"{f} <= ?", [c.value1]

    if c.operator == "Contains":
        return f"CAST({f} AS TEXT) LIKE ?", [f"%{c.value1}%"]

    if c.operator == "Starts With":
        return f"CAST({f} AS TEXT) LIKE ?", [f"{c.value1}%"]

    if c.operator == "Ends With":
        return f"CAST({f} AS TEXT) LIKE ?", [f"%{c.value1}"]

    if c.operator == "Between":
        return f"{f} BETWEEN ? AND ?", [c.value1, c.value2]

    if c.operator == "Is Null":
        return f"{f} IS NULL", []

    if c.operator == "Not Null":
        return f"{f} IS NOT NULL", []

    return "", []


def build_where(filters):
    sql = []
    params = []

    for i, c in enumerate(filters):
        s, p = build_condition(c)
        if not s:
            continue

        if i > 0:
            sql.append(c.logical_op)

        sql.append(s)
        params.extend(p)

    return (" WHERE " + " ".join(sql)) if sql else "", params