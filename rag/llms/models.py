from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

def setup_qa_pipeline(model_name: str = "google/gemma-2-2b-it") -> pipeline:
    """
    Setup question & answer pipeline.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    llm_model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
    qa_pipeline = pipeline("text-generation", model=llm_model, tokenizer=tokenizer)
    return qa_pipeline
