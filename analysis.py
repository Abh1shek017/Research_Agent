import re
from collections import Counter
import anthropic

# Define stopwords to exclude from the top terms display
STOPWORDS = {
    "the", "and", "of", "to", "in", "a", "is", "it", "for", "on", "that", "this",
    "with", "as", "are", "was", "by", "at", "an", "be", "from", "or", "which",
    "has", "have", "its", "but", "not", "can", "will", "their", "we", "our", "they"
}

def analyze_paper(text: str):
    # Extract all words (minimum 2 letters, alphabetic)
    words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())

    # Count all words for word_count (including stopwords)
    word_count = len(words)

    # Count word frequencies
    word_freq = Counter(words)

    # Remove stopwords for common terms
    filtered_freq = {word: freq for word, freq in word_freq.items() if word not in STOPWORDS}
    common_terms = Counter(filtered_freq).most_common(10)

    # Estimate references from "et al." and citations like [1], [2]
    reference_count = len(re.findall(r'\bet al\b|\[\d+\]', text, flags=re.IGNORECASE))

    return {
        "word_count": word_count,
        "common_terms": common_terms,
        "references": reference_count
    }
# Replace the local summarizer with this (using Claude API example)
import anthropic

def summarize(text: str) -> str:
    client = anthropic.Anthropic(api_key="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")
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"Summarize this research excerpt in bullet points:\n{text}"
        }]
    )
    return response.content[0].text

def extract_citations(text: str) -> list:
    """Extracts citation markers like [1], [2-5] etc."""
    return list(set(re.findall(r'\[(\d+[-–]?\d*)\]', text)))