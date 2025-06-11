import os
from typing import List, Dict
from .chunk import chunk_by_sections, fallback_chunk
from .translate import translate_text

def process_document(file_path: str, metadata: dict, engine: str = "libre") -> List[Dict]:
    """Process a single document and return a list of translated chunk dicts."""

    # Open and read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split the text into sections based on legal section markers
    sections_patterns = [r'(Article\s+\d+)', r'(Art\.\s*\d+)', r'(§+\s*\d+)']
    sections = chunk_by_sections(text, sections_patterns)

    # If no sections were found, fall back to character-based chunking
    section_based = True
    if not sections:
        sections = fallback_chunk(text)
        section_based = False

    # Extract the document ID (filename without path)
    doc_id = os.path.basename(file_path)

    # List to store all chunks as dictionaries
    chunks = []

    # Iterate over each chunk and prepare it for output
    for idx, chunk in enumerate(sections):
        if section_based:
            section_title, chunk_text = chunk # Extract the title and text for section-based chunks
        else:
            section_title = "undefined" # If fallback chunking is used, title is "undefined"
            chunk_text = chunk

        # Translate the chunk of text
        translated_chunk = translate_text(chunk_text, engine)
        translated_title = translate_text(metadata['title'], engine)

        # Create a dictionary containing metadata and chunk information
        chunks.append({
            "title": translated_title,
            "display_name": metadata.get('displayAddress',''),
            "keywords": metadata.get('keywords', ''),
            "announcementDate": metadata.get('announcementDate',''),
            "changeDate": metadata.get('changeDate', ''),
            "document_id": doc_id,
            "chunk_id": idx,
            "text": chunk_text,
            "chunk_title": section_title,
            "translated_text": translated_chunk
        })
    # Return the list of chunk dictionaries
    return chunks



def process_folder(folder_path: str, output_path: str, metadata: List[dict]):
    """
    This function processes all markdown (.md) files in a given folder, applies
    the chunking and translation functions, and saves the results to a JSONL file.
    Metadata need to contain year, pos and title.
    displayAdress, keywords, annoucementDate and changeDate are optional
    """
    all_chunks = [] # List to store all chunks from all files

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Process only .md files
        if filename.endswith('.md'):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing {file_path}...")
            # Find the correct metadata for the file based on naming convention
            for meta in metadata:
                if f'DU_{meta["year"]}_{meta["pos"]}.md' == filename:
                    chunks = process_document(file_path, meta)
                    break
            # Add the chunks to the list of all chunks
            try:
                 all_chunks.extend(chunks)
            except Exception as e:
                print(e) # Handle errors during chunk processing

    # Save the processed chunks to a JSONL (JSON Lines) file
    import json
    with open(output_path, 'w', encoding='utf-8') as f_out:
        for chunk in all_chunks:
            f_out.write(json.dumps(chunk) + '\n')
    # Print the number of chunks saved
    print(f"Saved {len(all_chunks)} chunks to {output_path}.")
