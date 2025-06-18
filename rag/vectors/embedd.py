from typing import List, Tuple, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoTokenizer
import torch


def embed_texts(
    texts: List[str],
    mode: str = 'document'
) -> Tuple[Union[np.ndarray, List[List[Tuple[str, np.ndarray]]]], Union[SentenceTransformer, AutoModel]]:
    """
    This function converts a list of text strings into numerical format (called embeddings),
    which makes it possible to compare the meaning of texts.

    Parameters:
    - texts: a list of English sentences or phrases.
    - model_name: the name of the model used to generate the embeddings. Default is a small, efficient model.

    Returns:
    - An array of embeddings, each representing the meaning of a text input.
    """
    if mode == 'document':
        model = load_document_model()
        embeddings = model.encode(texts, convert_to_numpy=True)
        return embeddings, model

    elif mode == 'word':
        model_name = 'bert-base-uncased'
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

        all_token_embeddings = []

        for text in texts:
            inputs = tokenizer(text, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)
            token_embeddings = outputs.last_hidden_state.squeeze(0)  # (seq_len, hidden_size)
            tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'].squeeze(0))
            token_vecs = [
                (token, token_embeddings[idx].numpy()) for idx, token in enumerate(tokens)
            ]
            all_token_embeddings.append(token_vecs)

        return all_token_embeddings, model

    else:
        raise ValueError("Invalid mode. Choose 'document' or 'word'.")

def load_document_model(model_name: str = 'all-mpnet-base-v2') -> SentenceTransformer:
    """
    Loads a sentence-transformers model suitable for document embeddings.
    """
    return SentenceTransformer(model_name)