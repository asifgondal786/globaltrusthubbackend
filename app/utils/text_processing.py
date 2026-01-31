"""
Text Processing Utilities
Text analysis, sanitization, and NLP helpers.
"""

import re
from typing import List, Optional, Tuple
import unicodedata


def sanitize_text(text: str) -> str:
    """
    Sanitize user input text.
    - Remove control characters
    - Normalize unicode
    - Trim whitespace
    """
    # Normalize unicode
    text = unicodedata.normalize("NFC", text)
    
    # Remove control characters except newlines and tabs
    text = "".join(
        char for char in text
        if not unicodedata.category(char).startswith('C')
        or char in '\n\t'
    )
    
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def extract_urls(text: str) -> List[str]:
    """Extract all URLs from text."""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)


def extract_emails(text: str) -> List[str]:
    """Extract all email addresses from text."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)


def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text."""
    # Various phone number patterns
    patterns = [
        r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-555-555-5555
        r'\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}',  # (555) 555-5555
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # 555-555-5555
        r'\d{4}[-.\s]?\d{7}',  # Pakistan format: 0300-1234567
    ]
    
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, text))
    
    return list(set(results))


def mask_sensitive_data(text: str) -> str:
    """
    Mask sensitive information in text.
    Used for logging and display purposes.
    """
    # Mask email addresses
    text = re.sub(
        r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        r'\1***@\2',
        text
    )
    
    # Mask phone numbers (keep first and last 2 digits)
    def mask_phone(match):
        num = match.group()
        if len(num) > 4:
            return num[:2] + '*' * (len(num) - 4) + num[-2:]
        return num
    
    text = re.sub(r'\+?\d{10,15}', mask_phone, text)
    
    # Mask CNIC (Pakistani national ID)
    text = re.sub(
        r'(\d{5})-?(\d{7})-?(\d)',
        r'\1-*******-\3',
        text
    )
    
    return text


def detect_language(text: str) -> str:
    """
    Simple language detection based on character analysis.
    Returns: 'en', 'ur', 'ar', or 'unknown'
    """
    # Count character types
    arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
    urdu_specific = len(re.findall(r'[\u0679\u067E\u0686\u0688\u0691\u0698\u06AF\u06C1\u06CC\u06D2]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    total = arabic_chars + english_chars
    if total == 0:
        return 'unknown'
    
    if urdu_specific > 0:
        return 'ur'
    if arabic_chars > english_chars:
        return 'ar'
    return 'en'


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts using Jaccard similarity.
    Returns value between 0 (no similarity) and 1 (identical).
    """
    # Tokenize
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].rsplit(' ', 1)[0] + suffix


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract key terms from text.
    Simple implementation using word frequency.
    """
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'can', 'to', 'of',
        'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'or',
        'and', 'but', 'if', 'then', 'so', 'than', 'too', 'very', 'just',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that',
    }
    
    # Tokenize and filter
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    words = [w for w in words if w not in stop_words]
    
    # Count frequency
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:max_keywords]]


# Scam detection patterns
SCAM_PATTERNS = [
    (r'send\s+money\s+first', 'payment_first'),
    (r'guaranteed\s+(visa|admission|job)', 'false_guarantee'),
    (r'100%\s+(success|guarantee)', 'unrealistic_promise'),
    (r'western\s+union|moneygram', 'suspicious_payment'),
    (r'act\s+(now|fast|immediately)', 'urgency_pressure'),
    (r'secret\s+(deal|opportunity)', 'secret_offer'),
    (r'limited\s+time\s+only', 'artificial_scarcity'),
    (r'no\s+(verification|documents)\s+needed', 'no_verification'),
]


def detect_scam_language(text: str) -> List[Tuple[str, str]]:
    """
    Detect potential scam language patterns.
    
    Returns:
        List of (matched_text, pattern_type) tuples
    """
    text_lower = text.lower()
    matches = []
    
    for pattern, pattern_type in SCAM_PATTERNS:
        found = re.findall(pattern, text_lower)
        if found:
            matches.append((found[0] if isinstance(found[0], str) else found[0][0], pattern_type))
    
    return matches
