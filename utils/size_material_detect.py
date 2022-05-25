import re

SIZE_VARIANT = {"size", "kích thước", "kích cỡ"}


def get_size_by_variant(variants):
    for variant in variants:
        for item in SIZE_VARIANT:
            if item in variant["name"].lower():
                size = ", ".join(variant["options"])
                size = re.sub(r'[\n\r\t]', '', size)
                return size
    return ""

def get_size_by_variant_tiki(variants):
    for variant in variants:
        for item in SIZE_VARIANT:
            if item in variant["name"].lower():
                size = ", ".join([i['label'] for i in variant['values']])
                # size = ", ".join(variant["options"])
                size = re.sub(r'[\n\r\t]', '', size)
                size = size.strip()
                return size
    return ""

def get_size_by_description(description):
    reg = r"(kích thước|kích cỡ|size)((\s|:|-|\|)+)(.+?)\s\|\|"
    result = re.findall(reg, description.lower())
    if result:
        return result[0][3].strip()
    return ""


def get_material_by_description(description):
    reg = r"(chất liệu|nguyên liệu|material)((\s|:|-|\|)+)(.+?)\s\|\|"
    result = re.findall(reg, description.lower())
    if result:
        return result[0][3].strip()
    return ""


