"""
Scam Language Analysis - NLP Preprocessing
Text preprocessing for scam detection.
"""

from typing import List, Tuple, Optional
import re
import unicodedata


# Scam indicator patterns by category
SCAM_PATTERNS = {
    "urgency": [
        r"\b(urgent|immediately|right now|asap|hurry|limited time)\b",
        r"\b(act fast|don't wait|expires|deadline|today only)\b",
    ],
    "false_guarantee": [
        r"\b(100%|guaranteed|definitely|certainly|surely)\b.*\b(visa|admission|job|success)\b",
        r"\b(no risk|risk.?free|money.?back)\b",
    ],
    "suspicious_payment": [
        r"\b(western union|moneygram|bitcoin|crypto|gift card)\b",
        r"\b(wire transfer|advance fee|processing fee|upfront)\b",
        r"\b(send money|transfer.*before|pay.*first)\b",
    ],
    "too_good": [
        r"\b(free visa|no documents|no test|no interview)\b",
        r"\b(no requirements|no experience needed|easy)\b",
        r"\b(instant approval|same day|express processing)\b",
    ],
    "pressure": [
        r"\b(only \d+ slots?|few spots?|last chance|final offer)\b",
        r"\b(special offer|exclusive deal|limited spots?)\b",
    ],
    "secrecy": [
        r"\b(secret|confidential|don't tell|keep private)\b",
        r"\b(between us|just you|special arrangement)\b",
    ],
    "impersonation": [
        r"\b(official|government|embassy|authorized agent)\b(?!.*verified)",
        r"\b(certified|licensed|accredited)\b(?!.*verified)",
    ],
}

# Weights for different pattern categories
CATEGORY_WEIGHTS = {
    "urgency": 1.0,
    "false_guarantee": 1.5,
    "suspicious_payment": 2.0,
    "too_good": 1.5,
    "pressure": 1.0,
    "secrecy": 1.5,
    "impersonation": 1.2,
}


def clean_text(text: str) -> str:
    """
    Clean and normalize text for analysis.
    """
    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+', ' [URL] ', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' [EMAIL] ', text)
    
    # Remove phone numbers
    text = re.sub(r'\+?\d[\d\s\-]{8,}\d', ' [PHONE] ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove excessive punctuation
    text = re.sub(r'([!?.]){2,}', r'\1', text)
    
    return text.strip()


def tokenize(text: str) -> List[str]:
    """
    Simple word tokenization.
    """
    # Split on whitespace and punctuation
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens


def extract_ngrams(tokens: List[str], n: int = 2) -> List[str]:
    """
    Extract n-grams from token list.
    """
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = ' '.join(tokens[i:i + n])
        ngrams.append(ngram)
    return ngrams


def detect_patterns(
    text: str,
) -> List[Tuple[str, str, str]]:
    """
    Detect scam patterns in text.
    
    Returns:
        List of (category, matched_text, pattern) tuples
    """
    cleaned = clean_text(text)
    matches = []
    
    for category, patterns in SCAM_PATTERNS.items():
        for pattern in patterns:
            found = re.findall(pattern, cleaned, re.IGNORECASE)
            for match in found:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                matches.append((category, match, pattern))
    
    return matches


def calculate_scam_score(
    text: str,
) -> Tuple[float, List[dict]]:
    """
    Calculate scam probability score.
    
    Returns:
        Tuple[float, List[dict]]: (score 0-1, reasons)
    """
    matches = detect_patterns(text)
    
    if not matches:
        return 0.0, []
    
    # Calculate weighted score
    category_hits = {}
    for category, matched_text, pattern in matches:
        if category not in category_hits:
            category_hits[category] = []
        category_hits[category].append(matched_text)
    
    weighted_sum = 0.0
    reasons = []
    
    for category, hits in category_hits.items():
        weight = CATEGORY_WEIGHTS.get(category, 1.0)
        category_score = min(len(hits) * weight * 0.1, 0.3)  # Cap per category
        weighted_sum += category_score
        
        reasons.append({
            "category": category,
            "hits": hits,
            "contribution": category_score,
        })
    
    # Normalize to 0-1
    final_score = min(weighted_sum, 1.0)
    
    return final_score, reasons


def preprocess_for_model(
    text: str,
) -> dict:
    """
    Preprocess text for ML model input.
    
    Returns:
        dict with preprocessed features
    """
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    bigrams = extract_ngrams(tokens, 2)
    trigrams = extract_ngrams(tokens, 3)
    
    # Basic features
    features = {
        "text": cleaned,
        "tokens": tokens,
        "bigrams": bigrams,
        "trigrams": trigrams,
        "token_count": len(tokens),
        "char_count": len(cleaned),
        "exclamation_count": text.count('!'),
        "question_count": text.count('?'),
        "caps_ratio": sum(1 for c in text if c.isupper()) / max(len(text), 1),
        "numeric_ratio": sum(1 for c in text if c.isdigit()) / max(len(text), 1),
        "has_url": '[URL]' in cleaned,
        "has_email": '[EMAIL]' in cleaned,
        "has_phone": '[PHONE]' in cleaned,
    }
    
    # Pattern-based features
    pattern_matches = detect_patterns(text)
    for category in SCAM_PATTERNS.keys():
        features[f"has_{category}"] = any(m[0] == category for m in pattern_matches)
    
    return features


def get_risk_assessment(
    score: float,
    reasons: List[dict],
) -> dict:
    """
    Generate human-readable risk assessment.
    """
    if score >= 0.7:
        risk_level = "high"
        recommendation = "This message shows multiple scam indicators. Exercise extreme caution."
    elif score >= 0.4:
        risk_level = "medium"
        recommendation = "This message has some suspicious elements. Verify claims independently."
    elif score >= 0.2:
        risk_level = "low"
        recommendation = "Minor concerns detected. Proceed with normal verification."
    else:
        risk_level = "minimal"
        recommendation = "No significant scam indicators detected."
    
    return {
        "score": score,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "details": reasons,
    }
