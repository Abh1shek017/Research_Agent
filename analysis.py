import re
from collections import Counter

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
