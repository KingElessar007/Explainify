from transformers import pipeline
import re

# Loading models
generator = pipeline("text2text-generation", model="google/flan-t5-large")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_casual_response(user_prompt: str) -> str:
    prompt = (
        "You're a helpful assistant who explains things like you're talking to a friend.\n"
        "Break down the topic clearly using simple language, relatable examples, and a light tone.\n\n"
        f"Instruction:\n{user_prompt.strip()}\n"
        "Respond in 4-5 big paragraphs."
    )
    result = generator(prompt, max_new_tokens=500, do_sample=True, temperature=0.7)[0]['generated_text']
    return result.strip()

def generate_academic_response(user_prompt: str) -> str:
    prompt = (
        "You're a scholarly assistant with expertise in academic writing.\n"
        "Provide a formal, logically structured, and precise explanation using academic terminology.\n"
        "Ensure your response is objective and well-organized.\n\n"
        f"Instruction:\n{user_prompt.strip()}\n"
        "Respond in 4-5 well-developed paragraphs."
    )
    result = generator(prompt, max_new_tokens=500, do_sample=True, temperature=0.6)[0]['generated_text']
    return result.strip()

def polish_text(text: str) -> str:
    prompt = (
        "You are an expert editor.\n"
        "Polish the following text for clarity, grammar, and coherence:\n\n"
        f"\"\"\"\n{text.strip()}\n\"\"\""
    )
    result = generator(prompt, max_new_tokens=500, do_sample=True, temperature=0.7)[0]['generated_text']
    return result.strip()

def summarize_text(text: str) -> str:
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text'].strip()

# cleaning function to remove unwanted characters and spaces
def clean_generated_text(text: str) -> str:
    
    text = text.strip().strip('"').strip("'")
    text = re.sub(r'^"+|"+$', '', text)
    text = re.sub(r"^'+|'+$", '', text)
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    text = re.sub(r'[\.\!\?][^\.!\?]*$', lambda m: m.group(0)[0], text)
    return text.strip()


def generate_both_summaries(user_prompt: str) -> dict:
    """
    Generate, polish, and summarize both casual and academic responses.
    Returns:
        dict: {'casual_summary': ..., 'academic_summary': ...}
    """
    # Casual
    casual = generate_casual_response(user_prompt)
    casual_polished = polish_text(casual)
    casual_summary = summarize_text(casual_polished)
    casual_summary = clean_generated_text(casual_summary)
    
    # Academic
    academic = generate_academic_response(user_prompt)
    academic_polished = polish_text(academic)
    academic_summary = summarize_text(academic_polished)
    academic_summary = clean_generated_text(academic_summary)
    
    return {
        "casual_summary": casual_summary,
        "formal_summary": academic_summary,
    }


# if __name__ == "__main__":
#     test_prompt = "Explain the term Artificial Intelligence (AI)."
#     print(generate_both_summaries(test_prompt))




# def summarize_text(text: str) -> str:
#     # Prompt engineering for summarization with FLAN-T5
#     prompt = (
#         "Summarize the following text in a clear, concise, and informative way:\n\n"
#         f"{text.strip()}\n\n"
#         "Summary:"
#     )
#     result = generator(prompt, max_new_tokens=300, do_sample=False)[0]['generated_text']
#     return result.strip()