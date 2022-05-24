import json
import os
import re
import time
import datetime
from typing import List
from utils.api_base import APIBase
from config import TIKI_API_ENDPOINT, FOLDER_OUTPUT, CHECKPOINT, TIKI_CATEGORY_IGNORE, TIKI_API_PRODUCT_DETAIL, USER_AGENT
from category.tiki_category import TIKI_CATEGORY
from product import Product, init_product_file_title
from multiprocessing import Pool


class TikiCrawler:
    __LIMIT_PAGE = 100

    def __init__(self, category_index: List):
        self.api_base = None
        self.list_category = []
        for index in category_index:
            self.list_category.append(TIKI_CATEGORY[index])
        self.config_api_base()
    
    def config_api_base(self):
        self.api_base = APIBase()
        self.api_base.set_max_retry(3)
        self.api_base.add_header({
            "Accept": "*/*",
            "User-Agent": USER_AGENT
        })

    def run(self):
        # get category need crawl
        for index, category in enumerate(self.list_category):
            print("======================")
            print(f"Crawling {index+1}/{len(self.list_category)}")
            print("======================")
            self.process_category(category)
    
    def process_category(self, category):
        if not CHECKPOINT:
            react_checkpoint = True
        else:
            react_checkpoint = False
        cate_main = category["item"]
        cate_sub = category["sub"]
        catesub_count = 0
        # crawl sub category
        for sub_detail in cate_sub:
            catesub_count += 1
            catesubsub_count = 0
            sub_sub_detail = sub_detail["sub"]
            for item_sub in sub_sub_detail:
                catesubsub_count += 1
                # start from checkpoint
                if not react_checkpoint and item_sub["item"]["title"] != CHECKPOINT:
                    print("Skipping ", item_sub["item"]["title"])
                    continue
                else:
                    react_checkpoint = True

                category_tree = [
                    cate_main["title"].replace("/", "-"),
                    item_sub["item"]["title"].replace("/", "-")
                ]
                cate_url = item_sub["item"]["url"]
                category_id = convert_tiki_url_to_category(cate_url)

                # check ignore category
                if not category_id or item_sub["item"]["id"] in TIKI_CATEGORY_IGNORE:
                    print("ignore category:", category_id, item_sub["item"]["title"])
                    continue

                print(f"=> l2: {catesub_count}/{len(cate_sub)}: l3: {catesubsub_count}/{len(sub_sub_detail)} {category_tree} id: {category_id}")
                
                # get all product in category
                self.save_product_by_category(category_tree, category_id)   

    def save_product_by_category(self, category_tree, category_id):
        folder_out = "{}/tiki/{}".format(FOLDER_OUTPUT, category_tree[0])
        if not os.path.isdir(folder_out):
            os.makedirs(folder_out)
        file_path = "{}/{}.csv".format(folder_out, category_tree[1])

        with open(file_path, "w+") as f:
            f.write(init_product_file_title())
            page_size = 1
            count_prod = 0
            while True:
                try:
                    list_product = self.get_list_product_by_category_page(category_tree, category_id, page_size)
                    if list_product is None or len(list_product) == 0:
                        break
                    count_prod += len(list_product)
                    print(category_tree, count_prod)
                    for prod in list_product:
                        f.write(prod.get_txt_append())
                except Exception as e:
                    print(str(e))
                    print("SLEEPING 10 MINUTE FROM:", datetime.datetime.now())
                    time.sleep(10*60)
                page_size += 1


    def get_list_product_by_category_page(self, category_tree, category_id, page_size):
        list_product = []
        param = {
            "limit": self.__LIMIT_PAGE,
            "category": category_id,
            "page": page_size,
            "aggregations": 2
        }
        res = self.api_base.get(url=TIKI_API_ENDPOINT, param=param, timeout=5)
        res = res.json()
        data = res.get("data")
        if not data:
            return list_product

        list_process = []
        for item in data:
            name = item.get("name")
            product = Product(name=name)
            product.category_tree = category_tree
            product.id = item.get("id")
            product.shop_id = item.get("seller_product_id")
            qty = item.get("stock_item")
            if qty:
                product.count = item["stock_item"].get("qty")
            sold = item.get("quantity_sold")
            if sold:
                product.sold = item["quantity_sold"].get("value")
            product.price = item.get("price")
            product.brand = item.get("brand_name").replace("\t", "")

            list_process.append(product)
        try:
            with Pool(20) as p:
                list_product = p.map(get_description_detail, list_process)
        except Exception as e:
            print("ERROR: ", category_tree, str(e))
        return list_product


def get_description_detail(p: Product):
    api_base = APIBase()
    api_base.add_header({
        "accept": "*/*",
        "user-agent": USER_AGENT
    })
    url = TIKI_API_PRODUCT_DETAIL.format(p.id)
    param = {
        "platform": "web"
    }
    res = api_base.get(url=url, param=param)

    if res.status_code == 200:
        res_json = res.json()
        p.description = res_json.get("description")
        # p.brand = res_json["brand"]["name"]
        specifications = res_json["specifications"]
        for spec in specifications:
            for attribute in spec["attributes"]:
                if attribute["code"] == "dimensions":
                    p.size = attribute["value"]
                elif attribute["code"] == "origin":
                    p.origin = attribute["value"]
                elif attribute["code"] == "manufacturer" and (not p.brand or p.brand == "OEM"):
                    p.brand = attribute["value"]
                elif attribute["code"] == "material":
                    p.material = attribute["value"]
                else:
                    for kt in ("kích thước", "kích cỡ", "size"):
                        if kt in attribute["name"].lower():
                            p.size == attribute["value"]

        variations = res_json.get("configurable_options")
        if variations:
            for v in variations:
                v.pop("position")
                v.pop("show_preview_image")
            p.variations = json.dumps(variations)

    api_base.req_session.close()
    return p


def convert_tiki_url_to_category(tiki_url):
    result = re.findall(r"\/c([0-9]+)\?", tiki_url)
    if result:
        return result[0]
    else:
        return None


if __name__ == '__main__':
    category_index = list(range(len(TIKI_CATEGORY)))
    print(category_index)
    tiki = TikiCrawler(category_index=category_index)
    tiki.run()
