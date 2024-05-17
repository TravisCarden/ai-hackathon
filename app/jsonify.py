import os
import sys
import json

def process_module(module_folder_path):
    module_folder_path = os.path.realpath(module_folder_path)

    if not os.path.isdir(module_folder_path):
        print("The provided path does not exist or is not a directory.")
        return

    module_name = os.path.basename(module_folder_path)
    output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    output_file_path = os.path.join(output_directory, f'{module_name}.contents_python.json')

    os.makedirs(output_directory, mode=0o755, exist_ok=True)

    file_data = []
    base_path_length = len(module_folder_path) + 1

    for root, _, files in os.walk(module_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = file_path[base_path_length:]
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
            except (UnicodeDecodeError, IOError):
                # Skip files that can't be read as text
                print(f"Skipping file due to decode error or IO error: {file_path}")
                continue

            file_data.append({
                'path': relative_path,
                'contents': contents
            })

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(file_data, f, indent=4, separators=(',', ': '), ensure_ascii=False)

    print(f"Module contents have been written to: {output_file_path}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        process_module(sys.argv[1])
    else:
        print("Please provide a directory path as an argument.")
