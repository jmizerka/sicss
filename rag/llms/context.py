import numpy as np

def prepare_chunks(data):
    chunks = []  # This will store the main content pieces
    titles = []  # This will store corresponding titles

    for item in data:
        # Get the English content and title. If not found, use default values.
        chunks.append(item.get('eng_chunk', ''))
        titles.append(item.get('eng_title', 'No title available'))

    return chunks, titles  # Return both content and title lists


def get_context_chunks(chunks, titles, indices):
    all_chunks = []  # This will store the final list of context chunks
    # Make sure indices are unique and flattened (single layer)
    unique_indices = np.unique(indices.flatten())
    for idx in unique_indices:
        current_chunk = chunks[idx]      # Main content piece
        current_title = titles[idx]      # Its title

        # Combine the main chunk and its surrounding context
        all_chunks.append({
            "chunk": current_chunk,
            "title": current_title,
        })

    return all_chunks  # Return list of documents with their context