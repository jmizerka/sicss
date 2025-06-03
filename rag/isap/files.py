from tqdm import tqdm
from typing import List
from .helpers import match_text_type, get_response


def save_article(doc: dict, file_ver: str, base_api_url: str, save_path: str) -> None:
    """
    A function to save specified version of the article in the provided path.
    """
    # If we have the official version ('U'), use that link
    if file_ver[0]:
        pdf_res = get_response(f'{base_api_url}/DU/{doc["year"]}/{doc["pos"]}/text/U/{file_ver[0]}', "pdf")
    # If we don’t have 'U' but have the original ('O'), use that one instead
    elif file_ver[1]:
        pdf_res = get_response(f'{base_api_url}/DU/{doc["year"]}/{doc["pos"]}/text/O/{file_ver[1]}', "pdf")
    # If neither version is available, try downloading the basic PDF
    else:
        pdf_res = get_response(f'{base_api_url}/DU/{doc["year"]}/{doc["pos"]}/text.pdf', "pdf")
    # Save the PDF file with a clear name that includes the publisher, year, and document number
    with open(f'{save_path}/DU_{doc["year"]}_{doc["pos"]}.pdf','wb') as f:
        f.write(pdf_res)


def get_articles(docs: List[dict], save_path: str) -> None:
    """
    This function downloads PDF versions of documents and saves them to specified path.
    It takes a list of documents and a place to save the files (save_path)
    """

    base_api_url = 'https://api.sejm.gov.pl/eli/acts'

    # Wrap the iteration with tqdm to show progress
    for doc in tqdm(docs, desc="Downloading PDFs"):
        #if there is no PDF file just skip it
        if not doc.get('textPDF'):
            continue
        file_versions = match_text_type(doc)
        save_article(doc, file_versions, base_api_url, save_path)


