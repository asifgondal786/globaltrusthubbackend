"""
Trust Score Engine - Behavior Analysis
Analyze user behavior patterns for trust scoring.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict


class BehaviorAnalyzer:
    """
    Analyze user behavior patterns to inform trust score.
    
    Monitors:
    - Response patterns (time, quality)
    - Interaction consistency
    - Red flags (suspicious patterns)
    - Positive indicators
    """
    
    def analyze_response_patterns(
        self,
        messages: List[Dict],
        user_id: str,
    ) -> Dict[str, float]:
        """
        Analyze message response patterns.
        
        Returns:
            Dict with response_time_avg, response_rate, consistency
        """
        if not messages:
            return {
                "response_time_avg": 0,
                "response_rate": 0,
                "consistency": 0,
            }
        
        # Calculate average response time
        response_times = []
        responded_count = 0
        
        for i, msg in enumerate(messages[:-1]):
            if msg.get("sender_id") != user_id:
                # Check if user responded
                next_msg = messages[i + 1]
                if next_msg.get("sender_id") == user_id:
                    responded_count += 1
                    # Calculate response time
                    time_diff = 300  # Placeholder - 5 minutes
                    response_times.append(time_diff)
        
        incoming_count = sum(1 for m in messages if m.get("sender_id") != user_id)
        
        return {
            "response_time_avg": sum(response_times) / len(response_times) if response_times else 0,
            "response_rate": responded_count / max(incoming_count, 1),
            "consistency": 0.8,  # Placeholder
        }
    
    def detect_suspicious_patterns(
        self,
        user_activity: List[Dict],
    ) -> List[Dict[str, any]]:
        """
        Detect suspicious behavior patterns.
        
        Checks for:
        - Rapid account activity (too fast for human)
        - Pattern matching with known scam behaviors
        - Inconsistent information
        - Unusual timing patterns
        """
        flags = []
        
        if not user_activity:
            return flags
        
        # Check for rapid activity (bot-like)
        timestamps = [a.get("timestamp") for a in user_activity if a.get("timestamp")]
        if len(timestamps) >= 10:
            # Check if too many actions in short time
            recent = timestamps[-10:]
            # If 10 actions in under 1 minute, flag as suspicious
            # Placeholder check
            pass
        
        # Check for bulk messaging
        messages_sent = [a for a in user_activity if a.get("type") == "message"]
        if len(messages_sent) > 50:  # More than 50 messages in session
            unique_recipients = set(m.get("recipient") for m in messages_sent)
            if len(unique_recipients) > 20:
                flags.append({
                    "type": "bulk_messaging",
                    "severity": "medium",
                    "details": f"Sent messages to {len(unique_recipients)} unique users",
                })
        
        # Check for profile changes
        profile_changes = [a for a in user_activity if a.get("type") == "profile_update"]
        if len(profile_changes) > 5:  # Frequent changes
            flags.append({
                "type": "frequent_profile_changes",
                "severity": "low",
                "details": f"{len(profile_changes)} profile changes detected",
            })
        
        return flags
    
    def calculate_interaction_quality(
        self,
        interactions: List[Dict],
    ) -> float:
        """
        Calculate quality score for user interactions.
        
        Returns:
            float: Quality score (0-1)
        """
        if not interactions:
            return 0.5  # Neutral for no data
        
        positive = 0
        negative = 0
        
        for interaction in interactions:
            outcome = interaction.get("outcome", "neutral")
            if outcome == "positive":
                positive += 1
            elif outcome == "negative":
                negative += 1
        
        total = len(interactions)
        if total == 0:
            return 0.5
        
        # Weight positive more than neutral
        quality = (positive * 2 + (total - positive - negative)) / (total * 2)
        
        return min(1.0, max(0.0, quality))
    
    def analyze_communication_style(
        self,
        messages: List[str],
    ) -> Dict[str, any]:
        """
        Analyze communication style for trust indicators.
        
        Checks:
        - Professional language use
        - Aggression or pressure tactics
        - Consistency in communication
        """
        if not messages:
            return {
                "professionalism": 0.5,
                "pressure_tactics": False,
                "aggressive_language": False,
            }
        
        all_text = " ".join(messages).lower()
        
        # Check for pressure tactics
        pressure_phrases = [
            "act now", "limited time", "urgent", "immediately",
            "don't miss", "last chance", "hurry",
        ]
        pressure_count = sum(1 for phrase in pressure_phrases if phrase in all_text)
        
        # Check for aggressive language
        aggressive_words = [
            "stupid", "idiot", "fool", "scam", "fraud",
            "waste", "terrible", "horrible",
        ]
        aggressive_count = sum(1 for word in aggressive_words if word in all_text)
        
        return {
            "professionalism": 0.7,  # Placeholder
            "pressure_tactics": pressure_count > 3,
            "aggressive_language": aggressive_count > 2,
            "pressure_score": pressure_count,
            "aggression_score": aggressive_count,
        }
    
    def get_behavior_summary(
        self,
        user_id: str,
        response_patterns: Dict,
        suspicious_flags: List,
        interaction_quality: float,
        communication_style: Dict,
    ) -> Dict[str, any]:
        """
        Generate comprehensive behavior summary.
        """
        # Calculate overall behavior score
        base_score = 0.5
        
        # Response quality impact
        if response_patterns.get("response_rate", 0) > 0.8:
            base_score += 0.1
        
        # Suspicious flags impact
        base_score -= len(suspicious_flags) * 0.1
        
        # Interaction quality impact
        base_score += (interaction_quality - 0.5) * 0.2
        
        # Communication style impact
        if communication_style.get("pressure_tactics"):
            base_score -= 0.15
        if communication_style.get("aggressive_language"):
            base_score -= 0.15
        
        return {
            "user_id": user_id,
            "overall_score": max(0, min(1, base_score)),
            "response_patterns": response_patterns,
            "suspicious_flags": suspicious_flags,
            "interaction_quality": interaction_quality,
            "communication_style": communication_style,
            "risk_level": "high" if base_score < 0.3 else "medium" if base_score < 0.6 else "low",
        }


# Global behavior analyzer instance
behavior_analyzer = BehaviorAnalyzer()
