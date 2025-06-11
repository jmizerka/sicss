import json
import time
import requests
from urllib.parse import quote
from tqdm import tqdm  # Shows a progress bar during translation
import ipywidgets as widgets  # UI elements for Colab
from IPython.display import display  # Show widgets in the notebook

# URL for LibreTranslate API, if you're running it locally
LIBRETRANSLATE_URL = "http://localhost:5000/translate"

# Template for the Lingva API (translates from Polish to English)
LINGVA_URL_TEMPLATE = "https://lingva.ml/api/v1/pl/en/{}"

# Target language for translation
TARGET_LANG = "en"


def translate_with_libretranslate(text):
    """
    Translate a single string using the LibreTranslate API.
    Assumes the API is running locally.
    """
    try:
        response = requests.post(
            LIBRETRANSLATE_URL,
            json={
                "q": text,
                "source": "auto",
                "target": TARGET_LANG,
                "format": "text",
                "alternatives": 1,
                "api_key": ""  # No API key needed by default
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()  # Raise error if request fails
        return response.json().get("translatedText", "")
    except Exception as e:
        print(f"LibreTranslate error: {e}")
        return ""


def translate_with_lingva(text):
    """
    Translate a single string using the Lingva public API.
    This API does not require a key and is suitable for smaller jobs.
    """
    try:
        url = LINGVA_URL_TEMPLATE.format(quote(text))  # Safely encode the text
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("translation", "")
    except Exception as e:
        print(f"Lingva error: {e}")
        return ""


def translate_text(text, engine):
    """
    Wrapper function that selects which translation engine to use.
    Parameters:
        - text: The string to be translated.
        - engine: Either "Lingva" or "LibreTranslate"
    """
    if engine.lower() == "lingva":
        return translate_with_lingva(text)
    return translate_with_libretranslate(text)


def translate_all(input_file, output_file, engine="libre"):
    """
    Translates all lines in a JSONL file and saves the results.

    Parameters:
        - input_file: Path to the input .jsonl file.
        - output_file: Path to save the translated .jsonl file.
        - engine: Which translation engine to use ("Lingva" or "LibreTranslate").

    This function:
        1. Loads each JSON object from the input file.
        2. Translates the "text" field in each object.
        3. Saves the translation in a new field called "eng_chunk".
        4. Writes all objects to the output file.
    """
    print(f"Using '{engine}' for translation...")
    start_time = time.time()

    # Load data
    json_objects = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                try:
                    json_objects.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")

    if not json_objects:
        print("No valid JSON objects found. Exiting.")
        return

    # Extract the "text" field from each object
    texts_to_translate = [obj.get("text", "") for obj in json_objects]

    # Translate each text and collect results
    translations = []
    for text in tqdm(texts_to_translate, desc="Translating"):
        translated_text = translate_text(text, engine)
        translations.append(translated_text)

    # Add translations back into the original JSON objects
    for obj, translated_text in zip(json_objects, translations):
        obj["eng_chunk"] = translated_text.strip()

    # Save results to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in json_objects:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

    print(f"\nTranslation completed in {time.time() - start_time:.2f} seconds.")
    print(f"Output saved to {output_file}")

    # Show a preview of the first result
    if json_objects:
        print("\nSample translation:")
        print(f"Original text: {json_objects[0].get('text', 'N/A')}")
        print(f"Translated text: {json_objects[0].get('eng_chunk', 'N/A')}")


def show_ui():
    """
    Builds and displays a simple user interface in Google Colab using dropdowns and text fields.

    This lets the user:
        - Choose a translation engine.
        - Specify the input and output file paths.
        - Click a button to start translation.

    It runs the translate_all() function when the user clicks "Run Translation".
    """
    # Dropdown for engine selection
    engine_dropdown = widgets.Dropdown(
        options=["LibreTranslate", "Lingva"],
        value="Lingva",
        description="Engine:"
    )

    # Text input for file paths
    input_file_text = widgets.Text(
        value="input.jsonl",
        description="Input File:"
    )

    output_file_text = widgets.Text(
        value="output.jsonl",
        description="Output File:"
    )

    # Button to run translation
    run_button = widgets.Button(description="Run Translation")

    # Function that is called when the button is clicked
    def on_button_click(b):
        translate_all(
            input_file=input_file_text.value,
            output_file=output_file_text.value,
            engine=engine_dropdown.value
        )

    # Connect button to function
    run_button.on_click(on_button_click)

    # Show all widgets in the notebook
    display(engine_dropdown, input_file_text, output_file_text, run_button)
