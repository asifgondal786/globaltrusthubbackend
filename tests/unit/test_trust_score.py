"""
Unit Tests - Trust Score
Tests for trust score calculation.
"""

import pytest


def test_verification_score_calculation():
    """Test verification component score calculation."""
    from app.ai_ml.trust_score_engine.score_calculator import trust_calculator
    
    # Unverified user
    score = trust_calculator.calculate_verification_score(
        verification_level=0,
        documents_verified=0,
        identity_confirmed=False,
    )
    assert score == 0
    
    # Level 1 verified
    score = trust_calculator.calculate_verification_score(
        verification_level=1,
        documents_verified=1,
        identity_confirmed=False,
    )
    assert score > 0
    
    # Fully verified
    score = trust_calculator.calculate_verification_score(
        verification_level=3,
        documents_verified=5,
        identity_confirmed=True,
    )
    assert score == 200  # Max score


def test_transaction_score_calculation():
    """Test transaction component score calculation."""
    from app.ai_ml.trust_score_engine.score_calculator import trust_calculator
    
    # New user with no transactions
    score = trust_calculator.calculate_transaction_score(
        successful_transactions=0,
        failed_transactions=0,
        total_value=0,
        dispute_rate=0,
    )
    assert score == 0
    
    # User with successful history
    score = trust_calculator.calculate_transaction_score(
        successful_transactions=20,
        failed_transactions=0,
        total_value=5000,
        dispute_rate=0,
    )
    assert score > 100
    
    # User with disputes
    score = trust_calculator.calculate_transaction_score(
        successful_transactions=10,
        failed_transactions=2,
        total_value=1000,
        dispute_rate=0.15,
    )
    assert score < 100  # Penalized for disputes


def test_review_score_calculation():
    """Test review component score calculation."""
    from app.ai_ml.trust_score_engine.score_calculator import trust_calculator
    
    # No reviews
    score = trust_calculator.calculate_review_score(
        total_reviews=0,
        average_rating=0,
        verified_reviews=0,
    )
    assert score == 0
    
    # Excellent reviews
    score = trust_calculator.calculate_review_score(
        total_reviews=50,
        average_rating=4.8,
        verified_reviews=40,
    )
    assert score > 150


def test_total_score_calculation():
    """Test total trust score calculation."""
    from app.ai_ml.trust_score_engine.score_calculator import trust_calculator
    
    total, breakdown = trust_calculator.calculate_total_score(
        verification_score=150,
        transaction_score=100,
        review_score=80,
        activity_score=60,
        behavior_score=100,
    )
    
    assert 0 <= total <= 1000
    assert "verification" in breakdown
    assert "transactions" in breakdown


def test_trust_level_assignment():
    """Test trust level assignment from score."""
    from app.ai_ml.trust_score_engine.score_calculator import trust_calculator, TrustLevel
    
    assert trust_calculator.get_trust_level(0) == TrustLevel.UNVERIFIED
    assert trust_calculator.get_trust_level(100) == TrustLevel.UNVERIFIED
    assert trust_calculator.get_trust_level(200) == TrustLevel.BRONZE
    assert trust_calculator.get_trust_level(400) == TrustLevel.SILVER
    assert trust_calculator.get_trust_level(600) == TrustLevel.GOLD
    assert trust_calculator.get_trust_level(800) == TrustLevel.PLATINUM
    assert trust_calculator.get_trust_level(1000) == TrustLevel.PLATINUM


def test_score_decay_for_inactivity():
    """Test trust score decay from inactivity."""
    from app.ai_ml.trust_score_engine.decay_logic import trust_decay
    from datetime import datetime, timedelta
    
    # Recent activity - no decay
    decay, reason = trust_decay.calculate_inactivity_decay(
        last_activity=datetime.utcnow() - timedelta(days=7),
        current_score=500,
    )
    assert decay == 0
    
    # Extended inactivity - should decay
    decay, reason = trust_decay.calculate_inactivity_decay(
        last_activity=datetime.utcnow() - timedelta(days=60),
        current_score=500,
    )
    assert decay > 0


def test_improvement_tips_generation():
    """Test improvement tips generation."""
    from app.ai_ml.trust_score_engine.score_calculator import trust_calculator, TrustLevel
    
    breakdown = {
        "verification": 20,  # Low - should suggest verification
        "transactions": 50,
        "reviews": 40,
        "activity": 30,
        "behavior": 80,
    }
    
    tips = trust_calculator.get_improvement_tips(breakdown, TrustLevel.UNVERIFIED)
    assert len(tips) > 0
    assert any("verif" in tip.lower() for tip in tips)
