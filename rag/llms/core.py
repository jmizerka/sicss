from .context import get_context_chunks, prepare_chunks
from typing import List, Optional
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss

def generate( query: str, context_chunks: List[str], qa_pipeline: pipeline, generation_params: Optional[dict] = None,
              sys_prompt: str = "Use the following context to answer the question. Return only the answer and the title of the document the answer comes from. Nothing more.") -> str:
    """
    Function to generate an answer from a model.
    Default model - gemma2 always returns context in the answer so we don't need to do anything to retrieve it back.
    generation_params specifies additional parameters for generation (see transformers.pipeline docs)
    """
    # Start building a prompt (input text) to send to the AI model
    context = ""
    # Add each document with its title and content
    for i, chunk_set in enumerate(context_chunks):
        context += f"Document {i+1} - TITLE: {chunk_set['title']}\n"
        context += f"Content: {chunk_set['chunk']}\n"
    #Use the following context to answer the question. Return only the answer and the title of the document the answer comes from. Nothing more.
    prompt = f"""{sys_prompt}

    Context:
    {context}

    Question:
    {query}

    Answer:"""

    try:
        # check if generation_params is empty, then we need to convert it to empty dict
        generation_params = generation_params or {}
        # unpack optional parameters to use for text generation
        return qa_pipeline(prompt, **generation_params)[0]["generated_text"]

    except Exception as e:
        # If something goes wrong , show the error
        return f"Error generating response: {str(e)}"


def rag_search(query: str, index:faiss.IndexFlatL2, data:dict, embedding_model: SentenceTransformer, qa_pipeline:pipeline, k: int=3, params=None) -> str:
    """
    Main function to do RAG (Retrieval-Augmented Generation). K parameter specifies numbers of context chunks to use
    """
    # Step 1: Break data into chunks and get titles
    chunks, titles = prepare_chunks(data)

    # Step 2: Convert the user's question into a number format (embedding)
    # This helps the computer "understand" and compare meaning
    query_embedding = embedding_model.encode([query], convert_to_numpy=True)


    # Step 3: Use the index to find the top-k most relevant chunks
    # The index is a search engine that finds closest matches to the query embedding
    D, I = index.search(query_embedding, k=k)


    # Step 4: Add surrounding context to each matched chunk
    context_chunks = get_context_chunks(chunks, titles, I)

    response = generate(query, context_chunks, qa_pipeline, params)
    return response # Return the AI's answer



