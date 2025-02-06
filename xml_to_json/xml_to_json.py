import os
import json
import argparse
import xml.etree.ElementTree as ET

def validate_product_data(product):
    try:
        product_id = int(product.get("id", 0))
        price = float(product.get("price", 0))
        name = product.get("name", "").strip()
        category = product.get("category", "").strip()

        if product_id <= 0 or price <= 0 or not name or not category:
            return False
        return True
    except ValueError:
        return False

def parse_xml_file(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        products = []
        for product in root.findall("product"):
            product_data = {
                "id": product.find("id").text if product.find("id") is not None else None,
                "name": product.find("name").text if product.find("name") is not None else None,
                "price": product.find("price").text if product.find("price") is not None else None,
                "category": product.find("category").text if product.find("category") is not None else None,
                "description": product.find("description").text if product.find("description") is not None else None
            }

            if validate_product_data(product_data):
                products.append(product_data)
            else:
                print(f"Invalid data in {xml_file}, skipping product.")

        return products if products else None
    except ET.ParseError:
        print(f"Error parsing {xml_file}, skipping.")
        return None


def convert_xml_to_json(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir(input_dir):
        if file.endswith(".xml"):
            xml_path = os.path.join(input_dir, file)
            product = parse_xml_file(xml_path)

            if product:
                json_path = os.path.join(output_dir, file.replace(".xml", ".json"))
                with open(json_path, "w", encoding="utf-8") as json_file:
                    json.dump(product, json_file, indent=4)
                print(f"Converted {file} to JSON.")

def main():
    parser = argparse.ArgumentParser(description="Convert XML files to JSON with validation.")
    parser.add_argument("--input-dir", default="./input", help="Directory containing XML files.")
    parser.add_argument("--output-dir", default="./output", help="Directory to save JSON files.")
    args = parser.parse_args()

    convert_xml_to_json(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
