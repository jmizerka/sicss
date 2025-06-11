import os
import shutil
from tqdm import tqdm
from typing import List
from .discard import remove_after, remove_before, strip_markdown
from .tables import detect_markdown_table, markdown_table_to_csv

def extract_md_files(input_dir: str, output_dir:str) -> None:
    """
    The function extracts .md files from nested subfolders into the same folder
    """
    for file in os.scandir(input_dir):
        md_path = f'{file.path}/{file.name}.md'
        if os.path.exists(md_path):
            shutil.move(md_path, f'{output_dir}/{file.name}.md')


def process_documents(filter_docs: List[str],
                      source_folder: str,
                      output_folder: str,
                      remove_after_params: dict,
                     keep_tables=True) -> None:
    """
    Processes markdown files in the given folder, cleans and extracts Polish text,
    and saves the output to a specified destination.

    Parameters:
    - filter_docs: List of dictionaries, each with 'year', 'pos', and 'title' keys.
    - source_folder: Folder containing the markdown files to process.
    - output_folder: Folder where processed files will be saved.
    - remove_after_params: patterns to filter out - default_ending, start_pattern, signature_patterns
    """

    # This part is creating a dictionary where the keys are file names
    # and the values are the titles of the documents. The dictionary is built
    # from a list of documents called `filter_docs`.
    # Each document is assumed to have a 'year', 'pos' (position), and 'title'.
    titles = {f"DU_{doc['year']}_{doc['pos']}.md": doc['title'] for doc in filter_docs}

    files = list(os.scandir(source_folder))  # convert to list so tqdm can measure length

    # This part is scanning through files in a specific folder one by one.
    for file in tqdm(files, desc="Extracting text"):
        # For each file, open it and read its contents as a string.
        # The 'with' statement ensures that the file is properly closed after being read.
        with open(os.path.join(source_folder, file.name), 'r', encoding='utf-8') as f:
            text = f.read()
        title = titles[file.name]
        text = remove_before(text, title)
        text = remove_after(text, remove_after_params)

        if not keep_tables:
            tables = detect_markdown_table(text)
    
            for i, table_idx in enumerate(tables):
                table = text[table_idx[0]:table_idx[1]]
                csv_table = markdown_table_to_csv(table)
                text = text.replace(table, f'Tabela {i}. {csv_table}\n')

        text = strip_markdown(text)
        # After processing the text, it is saved to a new file with the same name
        # in the 'output_folder'.
        output_path = os.path.join(output_folder, file.name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
