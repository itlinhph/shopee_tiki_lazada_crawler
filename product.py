import re
from utils.unit_name_detect import get_unit_name_by_product_name
from utils.size_material_detect import get_size_by_description, get_size_by_variant, get_material_by_description


class Product:
    def __init__(self, name):
        self.name = name
        self.unit_name = get_unit_name_by_product_name(name)
        self.id = None
        self.shop_id = None
        self.count = 0
        self.sold = 0
        self.size = ""
        self.material = ""
        self.brand = "No Brand"
        self.category_tree = []
        self.price = 0
        self.origin = ""
        self.variations = ""  # json
        self.variation_raw = {}
        self.description = ""

    def get_category_str(self):
        return " > ".join(self.category_tree)

    def get_name_clean(self):
        new = re.sub(r"(\(.+?\)|\[.+?\])", " ", self.name)
        new = re.sub(r'[^a-zA-Z0-9\sạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđAÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬOÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢEÈÉẺẼẸÊỀẾỂỄỆUÙÚỦŨỤƯỪỨỬỮỰIÌÍỈĨỊYỲÝỶỸỴĐÁàổọẻ,-\/\\*\.:–]', ' ', new)
        new = re.sub(r'(freeship|FREESHIP|FreeShip|Free Ship|free ship|FREE SHIP|\s+)', " ", new)
        return new.strip()

    def get_description_clean(self):
        return re.sub(r'[\n\r\t]', ' || ', self.description)

    def get_txt_append(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
            self.get_name_clean(),
            self.get_category_str(),
            self.brand,
            self.price,
            self.sold,
            self.count,
            self.unit_name,
            self.id,
            self.shop_id,
            self.get_size_clean(),
            self.material,
            self.origin,
            self.variations,
            self.get_description_clean()
        )

    def get_size_clean(self):
        size = re.sub(r'(\<.+?\>|\n|\r|\t)', ' ', self.size)
        # size = re.sub(r'[\n\r\t]', ' || ', size)
        return size

    def get_size(self):
        if self.size:
            return self.size
        size = get_size_by_variant(self.variations)
        if not size:
            size = get_size_by_description(self.description)
        return size

    def get_material(self):
        if self.material:
            return self.material
        return get_material_by_description(self.description)

    def get_export_file_format(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\n".format(
            self.unit_name,
            self.get_name_clean(),
            self.get_category_str(),
            self.brand,
            self.get_size(),
            self.get_material(),
        )


    def get_export_tiki_format(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
            self.unit_name,
            self.get_name_clean(),
            self.get_category_str(),
            self.brand,
            self.origin,  # for tiki
            self.get_size(),
            self.get_material(),
        )


def init_product_file_title():
    return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
        "name", "category", "brand", "price", "unit_sold", "unit_remain", "unit", "prod_id", "shop_id", "size", "material", "origin", "variations", "description"
    )


def init_title_export_file():
    return "{}\t{}\t{}\t{}\t{}\t{}\n".format(
        "Đơn vị", "Tên Sản Phẩm", "Loại mặt hàng", "Nhãn hiệu", "Kích thước", "Chất liệu"
    )


def init_tiki_export_file():
    return "{}\t{}\t{}\t{}\t{}\t{}\n".format(
        "Đơn vị", "Tên Sản Phẩm", "Loại mặt hàng", "Nhãn hiệu", "Xuất xứ", "Kích thước", "Chất liệu"
    )