import numpy as np
import faiss

def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    This function builds a searchable index from the text embeddings using FAISS,
    which allows for fast similarity searches.

    Parameters:
    - embeddings: the numerical representations of text.

    Returns:
    - A FAISS index ready for searching similar texts.
    """
    dim = embeddings.shape[1]  # Get the size of each embedding vector
    index = faiss.IndexFlatL2(dim)  # Create a flat index that uses Euclidean distance (L2) to measure similarity
    index.add(embeddings)  # Add the embeddings to the index
    return index

def save_faiss_index(faiss_index, index_path) -> None:
    """
    This function saves the FAISS index and the associated texts to files so they can be reused later.

    Parameters:
    - index: the FAISS index containing the embeddings.
    - texts: the original list of text chunks.
    - index_path: file path where the index should be saved.
    - texts_path: file path where the text list should be saved.
    """
    faiss.write_index(faiss_index, index_path)  # Save the index to a file

def read_faiss_index(index_path: str):
    """
    Reads faiss index from a file
    """
    index = faiss.read_index(index_path)
    return index