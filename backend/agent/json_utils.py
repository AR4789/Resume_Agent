import json
import re

def extract_json(text: str):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        return json.loads(match.group())
    except Exception:
        return None

def normalize_sections(sections: dict):
    normalized = {}

    for section, content in sections.items():
        items = []

        if isinstance(content, list):
            for entry in content:
                if isinstance(entry, str):
                    items.append(entry)
                elif isinstance(entry, dict):
                    # Flatten dict to readable bullets
                    for k, v in entry.items():
                        if isinstance(v, list):
                            for sub in v:
                                items.append(f"{k}: {sub}")
                        else:
                            items.append(f"{k}: {v}")

        normalized[section] = items

    return normalized
