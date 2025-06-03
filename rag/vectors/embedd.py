from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer

def embed_texts(texts: List[str], model_name: str = 'all-MiniLM-L6-v2') -> Tuple[np.ndarray, SentenceTransformer]:
    """
    This function converts a list of text strings into numerical format (called embeddings),
    which makes it possible to compare the meaning of texts.

    Parameters:
    - texts: a list of English sentences or phrases.
    - model_name: the name of the model used to generate the embeddings. Default is a small, efficient model.

    Returns:
    - An array of embeddings, each representing the meaning of a text input.
    """
    model = load_embedding_model(model_name)
    embeddings = model.encode(texts, convert_to_numpy=True)  # Convert texts into numerical vectors
    return embeddings, model

def load_embedding_model(model_name: str = 'all-MiniLM-L6-v2') -> SentenceTransformer:
    """
    Function loads embedding model from sentence_transformers.
    """
    model = SentenceTransformer(model_name)
    return model