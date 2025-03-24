import spacy
from config import SENSITIVE_EXTENSIONS, SENSITIVE_KEYWORDS

# Load spaCy's English NER model
nlp = spacy.load("en_core_web_sm")

def extract_sensitive_entities(text):
    """
    Extract sensitive entities using NER.
    Returns: List of sensitive entities (e.g., PERSON, EMAIL, CARD_NUMBER).
    """
    doc = nlp(text)
    sensitive_entities = []
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE", "EMAIL", "CARD_NUMBER"]:
            sensitive_entities.append((ent.text, ent.label_))
    return sensitive_entities

def tag_sensitive_files(file_path):
    """
    Tag sensitive files using NER and rule-based checks.
    Returns: True if sensitive, False otherwise.
    """
    # Rule 1: Check file extension
    if any(file_path.endswith(ext) for ext in SENSITIVE_EXTENSIONS):
        return True

    # Rule 2: Check file content with NER
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Check for sensitive keywords
            if any(keyword in content.lower() for keyword in SENSITIVE_KEYWORDS):
                return True
            # Check for sensitive entities using NER
            if extract_sensitive_entities(content):
                return True
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return False