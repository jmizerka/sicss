from langdetect import detect, detect_langs


def extract_lang(text: str, target_lang: str) -> str:
    """
    Function to keep only the text written in a specific language (e.g., Polish) from a larger text
    """
    # Break the full text into separate paragraphs (based on line breaks)
    paragraphs = text.split('\n')
    text = []

    # Go through each paragraph one by one
    for paragraph in paragraphs:
        if paragraph:  # Make sure the paragraph is not empty
            try:
                # Try to detect the language of this paragraph
                lang = detect(paragraph)
                # If it's written in the target language (e.g., Polish), keep it
                if lang == target_lang:
                    text.append(paragraph)
            except Exception:
                # If something goes wrong (e.g., unreadable text), just skip it
                continue
    # Return all the paragraphs that matched the target language, combined into one text block
    return '\n'.join(text)

def detect_lang_with_prob(text: str) -> str:
    return detect_langs(text)