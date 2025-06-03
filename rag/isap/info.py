from .helpers import get_response, calc_offset_incr
from tqdm import tqdm
from typing import Optional, List

def extract_all_docs_data(years_to_keep:Optional[list]=None) -> List[dict]:
    """
    Gets all years for which documents are available, loops through them from each year extracts all documents info.
    Allows for optional years filter - extract only docs information from years specified in years_to_keep
    """
    years = get_response('https://api.sejm.gov.pl/eli/acts/DU')['years']
    if years_to_keep:
        years = [year for year in years if year in years_to_keep]

    docs_info = []

    #tqdm adds progress bar
    for year in tqdm(years, desc="Processing years"):
        acts_count = get_response(f'https://api.sejm.gov.pl/eli/acts/DU/{year}')['count']
        limit = 500 # max number of concurrent documents to extract
        num_of_repeats = calc_offset_incr(acts_count, limit)

        for rep_num in tqdm(range(num_of_repeats), desc=f"Year {year}", leave=False):
            offset = limit * rep_num
            docs_response = get_response(
                f'https://api.sejm.gov.pl/eli/acts/search?limit={limit}&offset={offset}&publisher=DU&year={year}'
            )
            docs_info.extend(docs_response['items'])

    return docs_info

def filter_out_results(in_data: List[dict], filters:Optional[dict]=None) -> List[dict]:
    """
    Function to filter out documents matching given criteria. Criteria are defined by filters
    and may relate to status, type, title or inForce status of a document
    """
    if filters is None:
        filters = {}

    # extract values for each filter type
    statuses = filters.get('statuses')
    types = filters.get('types')
    titles = filters.get('titles')
    inforce_status = filters.get('inForce_status')

    out_data = []
    # for each document info in all documents
    for doc in in_data:
        # in python variables can be automatically evaluated as booleans
        # empty types evaluate to False: "", 0, None, [], {} etc
        if statuses and doc['status'] in statuses:
            continue
        if types and doc['type'] in types:
            continue
        if titles and any(keyword in doc['title'] for keyword in titles):
            continue
        if inforce_status is not None and doc['inForce'] == inforce_status:
            continue
        out_data.append(doc)

    return out_data