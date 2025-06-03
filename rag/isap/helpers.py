import requests
from typing import Union, Dict, Any, Tuple

def get_response(url: str, return_type: str ="json") -> Union[bytes, Dict[str, Any]]:
    """
    # This helper function contacts the API using a web address (URL)
    and returns the result as structured data (in JSON format) or file content (binary)
    """
    return requests.get(url).json() if return_type == "json" else requests.get(url).content


def calc_offset_incr(a: int, b: int) -> int:
    """
    This helper function calculates how many groups (chunks) of data we need
    It does this by dividing the total number of documents by how many we can get at once (500)
    The formula ensures we always round up, so we don’t miss any documents
    """
    return -(a // -b)


def match_text_type(doc: Dict[str, Any]) -> Tuple[str, str]:
    """
    This function checks which type of document we should download:
    - 'U' means the official (consolidated) version
    - 'O' means the original (announced) version
    We prefer the 'U' version if it’s available
    """
    file_o = file_u = None # We start by assuming we don't have either version

    # We go through the available text versions of this document
    for text in doc.get('texts', []):
        if text['type'] == 'U':
            file_u = text['fileName'] # Save the file name of the official version
            break  # # We found what we prefer, so we stop looking
        elif text['type'] == 'O':
            # If we don’t have 'U', we take the original version instead
            file_o = text['fileName']

    # Return both values (one of them might still be None)
    return file_u, file_o