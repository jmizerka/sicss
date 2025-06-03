import re
from typing import List, Tuple
import numpy as np

def chunk_by_sections(text: str, sections_patterns) -> List[Tuple[str, str]]:
    """Chunk text based on legal section markers, also keeping the section titles."""

    # Define patterns to identify section markers like "Article", "Art.", and "§".
    # Combine all the patterns into one, separated by a pipe, so that any of them can match.
    combined_pattern = '|'.join(sections_patterns)

    # Find all matches of the combined pattern in the text.
    matches = list(re.finditer(combined_pattern, text, re.IGNORECASE))

    # If no matches found, return an empty list.
    if not matches:
        return []

    # Initialize an empty list to store the chunked sections.
    chunks = []
    # Iterate over all matches to create chunks.
    for idx, match in enumerate(matches):
        section_title = match.group().strip()  # The title of the section (e.g., Article 1)
        start = match.start()  # The start index of the matched section
        # If it's not the last match, set the end to the start of the next match.
        # Otherwise, set the end to the length of the text.
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)

        # Extract the text chunk between the start and end indices.
        chunk_text = text[start:end].strip()

        # Append the section title and chunk of text to the chunks list.
        chunks.append((section_title, chunk_text))

    # Return the list of chunked sections.
    return chunks

def fallback_chunk(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Fallback to character-based chunking if no sections found."""
    chunks = []
    start = 0
    # Iterate over the text and divide it into chunks of the specified size
    while start < len(text):
        end = start + chunk_size  # Set the end index of the chunk
        chunk = text[start:end]   # Get the text for this chunk
        chunks.append(chunk.strip())  # Add the chunk to the list, stripping excess spaces
        start += chunk_size - overlap  # Move the starting index for the next chunk with overlap
    return chunks