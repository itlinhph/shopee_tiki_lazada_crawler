import time
import os
import json
from product import init_tiki_export_file, init_title_export_file, Product

CSV_RAW_INPUT = '/home/linhph/tiki_output/csv/'
CSV_PROCESSED_OUTPUT = '/home/linhph/tiki_output/csv_processed/'
XLSX_OUTPUT = '/home/linhph/tiki_output/xlsx/'
COUNT_ERROR = 0

def extract_csv_tiki_file(file_path):
    with open(file_path, "r") as f:
        contents = f.read().strip().split("\n")[1:]
    
    output_file = file_path.replace(CSV_RAW_INPUT, CSV_PROCESSED_OUTPUT)
    folder_out, _ = os.path.split(output_file)
    if not os.path.isdir(folder_out):
        os.makedirs(folder_out)
    with open(output_file, "w+") as f:
        f.write(init_tiki_export_file())
        for line in contents:
            try:
                # name, category, brand, _, _, _, unit, _, _, variation, description = line.split("\t")
                name, category, brand,_, _, _, _, prod_id, _, size,	material, origin, variation, description = line.split("\t")
                
                p = Product(
                    name=name,
                    brand=brand,
                    size=size,
                    material=material,
                    origin=origin,
                    category_tree=category.split(" > "),
                    description=description,
                )
                if variation:
                    p.variations = json.loads(variation)
                else:
                    p.variations = []
                new_line = p.get_export_tiki_format()
                f.write(new_line)
            except Exception as e:
                print(line)
                print(str(e))
                global COUNT_ERROR
                COUNT_ERROR+=1
                print("Number error: ", COUNT_ERROR)

def extract_csv_info():
    # get all csv files
    list_file = get_all_csv_file(CSV_RAW_INPUT)
    for file in list_file:
        print("Processing file:", file)
        extract_csv_tiki_file(file)


def get_all_csv_file(folder):
    list_file = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".csv"):
                list_file.append(os.path.join(root, file))
    return list_file



if __name__ == '__main__':
    stime = time.time()
    extract_csv_info()
    # run_convert_xlsx()
    print("Estimate: ", (time.time() - stime)/60, "minutes")
