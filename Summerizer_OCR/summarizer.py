from transformers import pipeline

# Load T5 summarization pipeline
summarizer=pipeline("summarization",model="t5-small",tokenizer="t5-small")

def summarize_text(text):
    
    text = text.strip().replace("\n", " ")
    max_input_words = 512

    if len(text.split()) > max_input_words:
        text = " ".join(text.split()[:max_input_words])
        
    summary = summarizer(text, max_length=100, min_length=25, do_sample=False)
    return summary[0]['summary_text']