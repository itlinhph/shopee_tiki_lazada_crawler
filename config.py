import time

# FOLDER_OUTPUT = "output" + str(int(time.time()))
FOLDER_OUTPUT = "/home/linhph/tiki_output/v3/"
CHECKPOINT = None

# FOR SHOPEE ONLY
SHOPEE_API_ENDPOINT = "https://shopee.vn/api/v4/search/search_items"
SHOPEE_API_PRODUCT_DETAIL = "https://shopee.vn/api/v2/item/get"

# FOR TIKI ONLY
TIKI_API_ENDPOINT = "https://tiki.vn/api/personalish/v1/blocks/listings"
TIKI_API_PRODUCT_DETAIL = "https://tiki.vn/api/v2/products/{}?platform=web"
# TIKI_CATEGORY_IGNORE = {442, 443, 444, 445, 1103, 446, 447, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612,
#                         1613, 1614, 1615, 1616, 1591, 1618, 1619, 1620, 1621, 1622, 1624, 1625, 1623, 468, 467, 469,
#                         466, 476, 472, 471, 480, 475, 477, 499, 500, 501, 502, 503,
#                         # tivi
#                         395, 843, 844, 396, 846, 845, 1106, 425, 426}

TIKI_CATEGORY_IGNORE = {}

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'