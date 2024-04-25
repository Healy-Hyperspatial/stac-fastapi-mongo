"""utilities for stac-fastapi.mongo."""

from base64 import urlsafe_b64decode, urlsafe_b64encode

from bson import ObjectId
from dateutil import parser  # type: ignore


def serialize_doc(doc):
    """Recursively convert ObjectId to string in MongoDB documents."""
    if isinstance(doc, dict):
        for k, v in doc.items():
            if isinstance(v, ObjectId):
                doc[k] = str(v)  # Convert ObjectId to string
            elif isinstance(v, dict) or isinstance(v, list):
                doc[k] = serialize_doc(v)  # Recurse into sub-docs/lists
    elif isinstance(doc, list):
        doc = [serialize_doc(item) for item in doc]  # Apply to each item in a list
    return doc


def decode_token(encoded_token: str) -> str:
    """Decode a base64 string back to its original token value."""
    token_value = urlsafe_b64decode(encoded_token.encode()).decode()
    return token_value


def encode_token(token_value: str) -> str:
    """Encode a token value (e.g., a UUID or cursor) as a base64 string."""
    encoded_token = urlsafe_b64encode(token_value.encode()).decode()
    return encoded_token


def convert_datetime(obj):
    """
    Recursively converts date strings in ISO 8601 format with timezone offsets into \
    date strings with 'Z' timezone indicator. The input can be either a dictionary or a list, \
    possibly nested, containing date strings.

    Args:
        obj (dict or list): The dictionary or list containing date strings to convert.

    Returns:
        dict or list: The converted dictionary or list with date strings in the desired format.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict) or isinstance(value, list):
                obj[key] = convert_datetime(value)
            elif isinstance(value, str):
                try:
                    parsed_value = parser.parse(value)
                    obj[key] = parsed_value.strftime("%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    pass  # If parsing fails, retain the original value
            elif value is None:
                obj[key] = None  # Handle null values
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            if isinstance(value, str):  # Only attempt to parse strings
                try:
                    parsed_value = parser.parse(value)
                    obj[i] = parsed_value
                except ValueError:
                    pass  # If parsing fails, retain the original value
            elif isinstance(value, list):
                obj[i] = convert_datetime(value)  # Recursively handle nested lists
    return obj
