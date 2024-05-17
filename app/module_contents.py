import os
import shutil
import subprocess
import tempfile
import json

def clone_and_convert_to_json(git_url):
    temp_dir = tempfile.mkdtemp()

    try:
        subprocess.run(['git', 'clone', git_url], cwd=temp_dir, check=True)
        module_name = git_url.split("/")[-1].split(".")[0]

        file_data = []
        routing_file_data = []
        skip_files = {'html', 'md', 'png', 'json', 'css', 'js'}

        for root, dirs, files in os.walk(os.path.join(temp_dir,module_name)):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.startswith('.'):
                    continue
                if any(word.lower() in file.lower() for word in skip_files):
                    continue
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, temp_dir)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contents = f.read()
                except (UnicodeDecodeError, IOError):
                    # Skip files that can't be read as text
                    print(f"Skipping file due to decode error or IO error: {file_path}")
                    continue

                if 'routing.yml' in file.lower():
                    routing_file_data.append({
                        'path': relative_path,
                        'contents': contents
                    })
                else:
                    file_data.append({
                        'path': relative_path,
                        'contents': contents
                    })



        return json.dumps(file_data, indent=4, separators=(',', ': '), ensure_ascii=False), json.dumps(routing_file_data, indent=4, separators=(',', ': '), ensure_ascii=False)
    finally:
        shutil.rmtree(temp_dir)
