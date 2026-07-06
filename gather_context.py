import os

# Folders to ignore so we don't read heavy dependencies or compiled files
ignore_dirs = {'.git', 'node_modules', '__pycache__', 'venv', 'env', '.vscode'}
# File types you want me to review
allowed_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.json', '.env.example'}

with open("project_context.txt", "w", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk("."):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in allowed_extensions):
                filepath = os.path.join(root, file)
                # Create a clear header for each file
                outfile.write(f"\n\n{'='*50}\n")
                outfile.write(f"FILE: {filepath}\n")
                outfile.write(f"{'='*50}\n\n")
                try:
                    with open(filepath, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"[Error reading file: {e}]\n")

print("Code consolidated into project_context.txt!")