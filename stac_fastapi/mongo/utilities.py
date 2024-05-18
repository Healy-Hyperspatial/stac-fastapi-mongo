"""utilities for stac-fastapi.mongo."""

from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import timezone

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


def parse_datestring(dt_str: str) -> str:
    """
    Normalize various ISO 8601 datetime formats to a consistent format.

    Args:
        dt_str (str): The datetime string in ISO 8601 format.

    Returns:
        str: The normalized datetime string in the format "YYYY-MM-DDTHH:MM:SSZ".
    """
    # Parse the datetime string to datetime object
    dt = parser.isoparse(dt_str)

    # Convert the datetime to UTC and remove microseconds
    dt = dt.astimezone(timezone.utc).replace(microsecond=0)

    # Format the datetime to the specified format
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
