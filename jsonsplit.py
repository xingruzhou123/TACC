import json
import os

# File to split
input_file = "vid2realreal1.json"
output_file1 = "vid2realreal_part1.json"
output_file2 = "vid2realreal_part2.json"

def calculate_json_size(obj):
    """Calculate approximate size of a JSON object in bytes."""
    return len(json.dumps(obj))

def split_json_balanced(input_file, output_file1, output_file2):
    # Load the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Handle only list or dictionary JSON structures
    if isinstance(data, list):
        part1, part2 = [], []
        size1, size2 = 0, 0

        for item in data:
            item_size = calculate_json_size(item)
            # Distribute items dynamically to balance size
            if size1 <= size2:
                part1.append(item)
                size1 += item_size
            else:
                part2.append(item)
                size2 += item_size

    elif isinstance(data, dict):
        part1, part2 = {}, {}
        size1, size2 = 0, 0

        for key, value in data.items():
            item_size = calculate_json_size({key: value})
            # Distribute items dynamically to balance size
            if size1 <= size2:
                part1[key] = value
                size1 += item_size
            else:
                part2[key] = value
                size2 += item_size
    else:
        raise ValueError("Unsupported JSON structure. Must be a list or a dictionary.")

    # Write each part to separate files
    with open(output_file1, 'w') as f:
        json.dump(part1, f, indent=4)
    with open(output_file2, 'w') as f:
        json.dump(part2, f, indent=4)

    # Output the sizes of the files
    size1 = os.path.getsize(output_file1)
    size2 = os.path.getsize(output_file2)
    print(f"{output_file1} size: {size1} bytes")
    print(f"{output_file2} size: {size2} bytes")

# Run the split function
split_json_balanced(input_file, output_file1, output_file2)
