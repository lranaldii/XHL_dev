import os
import re

def evaluate_contain(doc_type, file, keywords):
    """
    Checks whether a document contains all required keywords.
    Supports basic normalization for ICS and CSV files.
    """

    # File existence
    if not os.path.exists(file):
        return {
            "success": False,
            "reason": "file_not_found"
        }

    # Read file
    try:
        with open(file, "r", encoding="utf-8") as f:
            raw_content = f.read()
    except Exception as e:
        return {
            "success": False,
            "reason": "read_error",
            "error": str(e)
        }

    # Normalize content
    content = raw_content

    # ICS normalization
    if doc_type.lower() == "ics":
        # Unfold folded lines (RFC 5545)
        # Lines starting with space/tab are continuations
        content = re.sub(r"\r?\n[ \t]", "", content)

    # CSV normalization
    elif doc_type.lower() == "csv":
        # Normalize delimiters and spacing
        content = content.replace(";", ",")
        content = re.sub(r"[ \t]+", " ", content)

    # Case-insensitive matching
    content_lower = content.lower()

    missing = [
        k for k in keywords
        if k.lower() not in content_lower
    ]

    # Final result
    return {
        "success": len(missing) == 0,
        "missing_keywords": missing
    }
