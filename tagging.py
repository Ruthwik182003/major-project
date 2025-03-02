from config import SENSITIVE_EXTENSIONS, SENSITIVE_KEYWORDS

def tag_sensitive_files(file_path):
    """
    Tag sensitive files based on extensions and keywords.
    """
    if any(file_path.endswith(ext) for ext in SENSITIVE_EXTENSIONS):
        return True
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if any(keyword in content for keyword in SENSITIVE_KEYWORDS):
                return True
    except Exception as e:
        print(f"Failed to read file {file_path}: {e}")
    return False