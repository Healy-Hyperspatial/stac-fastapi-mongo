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


def parse_datestring(str):
    """Parse date string using dateutil.parser.parse() and returns a string formatted \
    as ISO 8601 with milliseconds and 'Z' timezone indicator.

    Args:
        str (str): The date string to parse.

    Returns:
        str: The parsed and formatted date string in the format 'YYYY-MM-DDTHH:MM:SS.ssssssZ'.
    """
    parsed_value = parser.parse(str)
    return parsed_value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def convert_obj_datetimes(obj):
    """Recursively explores dictionaries and lists, attempting to parse strings as datestrings \
    into a specific format.

    Args:
        obj (dict or list): The dictionary or list containing date strings to convert.

    Returns:
        dict or list: The converted dictionary or list with date strings in the desired format.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict) or isinstance(value, list):
                obj[key] = convert_obj_datetimes(value)
            elif isinstance(value, str):
                try:
                    obj[key] = parse_datestring(value)
                except ValueError:
                    pass  # If parsing fails, retain the original value
            elif value is None:
                obj[key] = None  # Handle null values
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            if isinstance(value, str):  # Only attempt to parse strings
                try:
                    obj[i] = parse_datestring(value)
                except ValueError:
                    pass  # If parsing fails, retain the original value
            elif isinstance(value, list):
                obj[i] = convert_obj_datetimes(value)  # Recursively handle nested lists
    return obj
