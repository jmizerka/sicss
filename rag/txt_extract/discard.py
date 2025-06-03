import re
from rapidfuzz import fuzz
from typing import List


def remove_before(content: str, title: str, threshold = 90):
    """
    Function to remove any unwanted content at the beginning of the text—such as fragments from other documents—
    that appear before the specified title.

    It uses the partial_ratio algorithm to compare each line of the text to the target title.
    If a line matches the title with over 90% similarity, everything preceding that line is discarded.
    """
    # remove common parts from the title to prevent false positives in matchining titles
    cleaned_title = re.sub(r'\s+z dnia\s+\d{1,2}\s+\w+\s+\d{4}\s+r\.', '', title)
    # Go through each line in the content to find where the actual document starts
    for idx, line in enumerate(content):
        # Compare how similar the current line is to the cleaned title (on a scale from 0 to 100)
        score = fuzz.partial_ratio(line.lower(), cleaned_title.lower())
        if score >= threshold:
            # Found the likely start — slice from the next line
            content_str = '\n'.join(content[idx + 1:])
            # Prepend the official title
            return f"{title}\n{content_str}"
    # If no matching title found, return the content unchanged
    return content


def remove_after(content: str,
                 params: dict) -> str:
    """
    This function cleans up texts by removing any unwanted text
    that may have been added after the main content — like footers, unrelated laws,
    or repeated signatures. It tries a few methods:
    - polish laws often end with a phrase "wchodzi w życie"
    - polish legal acts often start with type of a document
    - polish legal acts often end with a signature of the issuing person/authority
    """
    # Step 1: Check if the phrase 'wchodzi w życie' appears in the text.
    # This phrase usually signals the final sentence of a Polish legal act ("comes into force").
    default_ending = params.get('default_ending')
    start_pattern: str = params.get('start_pattern')
    signature_patterns: str = params.get('signature_patterns')

    if default_ending in content: #wchodzi w życie
        # Find the last occurrence of the phrase in the document
        end_position = content.rfind(default_ending)
        # Find the end of that line (i.e., where the newline character '\n' is located after that phrase)
        end_line_end = content.find('\n', end_position)
        # Cut off everything after that line and return the cleaned content
        return content[:end_line_end if end_line_end != -1 else len(content)].strip()

    # Step 2: If the above phrase wasn't found, check if a new law starts later in the text.
    # Acts in Journal of Laws are published as a book so sometimes one act may end
    # at the same page the next one starts

    # regular expression: ^ - start of the line, \s* - zero or more whitespaces
    # a{x,y} - matches character "a" exactly x or y times
    #start_pattern = r'^\s*#{2,3}\s*(USTAWA|ROZPORZĄDZENIE|OBWIESZCZENIE)'
    match = re.search(start_pattern, content, flags=re.MULTILINE)
    if match:
        # If we find such a heading, we assume the real content ends before it.
        end_position = match.start()
        return content[:end_position].strip()

    # Step 3: If neither of the above checks worked, look for official signatures.
    # These signatures usually appear at the end of a legal document,
    # so anything after them is likely unnecessary.


    for pattern in signature_patterns:
        match = re.search(pattern, content)
        if match:
            # If a signature is found, everything after that is probably not part of the main text
            end_position = match.start()
            return content[:end_position].strip()


    # If none of the checks found a clear endpoint, return the original text unchanged
    return content.strip()


def strip_markdown(text: str) -> str:
    """
    remove Markdown formatting, preserve only text
    """
    text = re.sub(r'!\[.*?]\(.*?\)', '', text)  # images
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)   # links
    text = re.sub(r'>\s?', '', text)             # quotes
    text = re.sub(r'#+\s?', '', text)            # headers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # italics
    text = re.sub(r'<[^>]+>', '', text)           # html tags
    text = re.sub(r'\n{2,}', '\n', text)           # multiple empty lines
    return text.strip()