import json

def replace_location_with_category(json_file_path, output_file_path=None):

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    valid_categories = ["Python", "SQL", "CS"] # TO DO: dynamic from SQL

    for key, details in data.items():
        if "location" in details:

            while True:
                print(f"\nTopic: {key}")
                print("Choose category for this topic:", valid_categories)
                category_input = input("Category: ").strip()
                if category_input in valid_categories:
                    details["category"] = category_input
                    break
                else:
                    print("Invalid category. Please choose from:", valid_categories)

            del details["location"]


    if output_file_path is None:
        output_file_path = json_file_path

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return data



updated_data = replace_location_with_category(
    "category_name_file_pairs.json",
    output_file_path="updated_data.json"
)
print("Updated JSON successfully!")
