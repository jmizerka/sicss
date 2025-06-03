import re

def detect_markdown_table(text):
    """
    Detect markdown tables
    This regex looks for rows that start and end with a pipe character ('|'), and are followed by one or more newline or carriage return characters.
    Explanation of the pattern:
     - (\|.*\|[\n\r]+):
         - \| : Matches the pipe character ('|').
         - .* : Matches any character (except newline) zero or more times. This matches the content between the pipes.
         - \| : Matches the closing pipe character ('|').
         - [\n\r]+ : Matches one or more newline (\n) or carriage return (\r) characters. This matches the end of the row.
    """

    # Pattern to detect tables
    table_pattern = r'(\|.*\|[\n\r]+)+'

    # Using re.finditer() to find all matches of the pattern in the input text.
    # finditer returns an iterator that produces match objects for every match in the text.
    matches = list(re.finditer(table_pattern, text))

    # Initialize an empty list to store the start and end positions of all the tables detected.
    tables = []

    # Loop through all the matches found
    for match in matches:
        # start() method gives the starting index of the match in the text.
        start_idx = match.start()
        # end() method gives the ending index of the match in the text.
        end_idx = match.end()
        # Append the start and end positions of the detected table as a tuple to the 'tables' list.
        tables.append((start_idx, end_idx))
    # Return the list of tables with their start and end positions in the text.
    return tables

def markdown_table_to_csv(text):
    """
    convert table into comma separated values format (csv)
    """
    # First, we clean up the input text by stripping any leading or trailing whitespace
    # Then, we split the text into separate lines using the newline character '\n'.
    lines = text.strip().split('\n')
    # Initialize an empty list to store the rows of the table in CSV format
    result = []

    # Loop through each line in the table
    for line in lines:
        # Skip the separator line (e.g., | --- | --- |) that typically appears in markdown tables
        # The separator line contains only hyphens ('-') and spaces, so we check if the line
        # (after removing all pipe '|' characters and trimming spaces) consists solely of hyphens or spaces.
        if set(line.replace('|', '').strip()) <= {'-', ' '}:
            continue

        # For each non-separator line:
        # - Remove leading and trailing pipe characters ('|') using strip('|')
        # - Split the line by the pipe character ('|') to get individual cells
        # - Strip any extra spaces from each cell using the strip() method
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        # Join the cells with a comma and a space (', ') to format them as a CSV row
        result.append(', '.join(cells))

    return '\n'.join(result)