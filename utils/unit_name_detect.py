from enum import Enum


class UnitName(Enum):
    CAI = "cái"
    CHIEC = "chiếc"
    CAP = "cặp"
    BO = "bộ"
    SET = "set"


DICT_PRODUCT_UNIT = {
    "đồng hồ": UnitName.CAI.value,
    "combo": UnitName.SET.value
}

LIST_DEFAULT_UNIT_NAME = ["cái", "chiếc", "cặp", "bộ", "set"]


def get_unit_name_by_product_name(product_name):
    prd_lower = product_name.lower()

    for item in LIST_DEFAULT_UNIT_NAME:
        if item in prd_lower:
            return item

    for key, value in DICT_PRODUCT_UNIT.items():
        if key in prd_lower:
            return value
    return UnitName.CAI.value
