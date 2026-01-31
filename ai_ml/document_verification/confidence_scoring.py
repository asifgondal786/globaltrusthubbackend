"""
Document Verification - Confidence Scoring
Calculate confidence scores for document verification.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class ConfidenceScorer:
    """
    Calculate confidence scores for document verification.
    
    Combines multiple signals:
    - OCR quality
    - Forgery analysis
    - Data consistency
    - Cross-reference verification
    """
    
    def __init__(self):
        self.auto_approve_threshold = 0.95
        self.auto_reject_threshold = 0.3
        self.review_required_min = 0.6
    
    def calculate_score(
        self,
        ocr_result: Dict[str, Any],
        forgery_result: Dict[str, Any],
        validation_result: Dict[str, Any],
        cross_reference: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Calculate overall confidence score.
        
        Args:
            ocr_result: OCR extraction results
            forgery_result: Forgery detection results
            validation_result: Field validation results
            cross_reference: Optional cross-reference check results
        
        Returns:
            Dict with confidence score and decision
        """
        scores = {}
        
        # OCR Quality Score (0-1)
        scores["ocr_quality"] = self._score_ocr_quality(ocr_result)
        
        # Forgery Score (inverted - high = no forgery)
        forgery_confidence = forgery_result.get("confidence", 0)
        scores["authenticity"] = 1.0 - forgery_confidence
        
        # Validation Score
        scores["validation"] = 1.0 if validation_result.get("is_valid") else 0.5
        
        # Cross-reference Score (if available)
        if cross_reference:
            scores["cross_reference"] = cross_reference.get("match_score", 0.5)
        
        # Calculate weighted average
        weights = {
            "ocr_quality": 0.2,
            "authenticity": 0.4,
            "validation": 0.25,
            "cross_reference": 0.15,
        }
        
        total_weight = sum(weights[k] for k in scores.keys())
        weighted_sum = sum(scores[k] * weights[k] for k in scores.keys())
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Determine decision
        decision = self._make_decision(overall_score, forgery_result)
        
        return {
            "overall_score": overall_score,
            "component_scores": scores,
            "decision": decision,
            "requires_manual_review": decision == "review",
            "auto_approved": decision == "approve",
            "auto_rejected": decision == "reject",
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def _score_ocr_quality(self, ocr_result: Dict[str, Any]) -> float:
        """Score OCR extraction quality."""
        base_confidence = ocr_result.get("confidence", 0)
        
        # Boost if key fields were extracted
        fields = ocr_result.get("fields", {})
        filled_fields = sum(1 for v in fields.values() if v is not None)
        total_fields = len(fields) if fields else 1
        
        field_ratio = filled_fields / total_fields
        
        return (base_confidence * 0.6 + field_ratio * 0.4)
    
    def _make_decision(
        self,
        score: float,
        forgery_result: Dict[str, Any],
    ) -> str:
        """
        Make verification decision.
        
        Returns: "approve", "reject", or "review"
        """
        # Reject if high forgery confidence
        if forgery_result.get("forgery_detected"):
            return "reject"
        
        # Auto-approve if high confidence
        if score >= self.auto_approve_threshold:
            return "approve"
        
        # Auto-reject if low confidence
        if score < self.auto_reject_threshold:
            return "reject"
        
        # Require manual review for middle ground
        return "review"
    
    def get_score_explanation(
        self,
        score_result: Dict[str, Any],
    ) -> List[str]:
        """
        Generate human-readable explanation of score.
        """
        explanations = []
        scores = score_result.get("component_scores", {})
        
        if scores.get("authenticity", 1) < 0.8:
            explanations.append("Potential authenticity concerns detected")
        
        if scores.get("ocr_quality", 1) < 0.7:
            explanations.append("Document quality may be insufficient")
        
        if scores.get("validation", 1) < 1.0:
            explanations.append("Some extracted fields could not be validated")
        
        if not explanations:
            explanations.append("Document passed all verification checks")
        
        return explanations
    
    def calculate_document_set_score(
        self,
        document_scores: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculate overall score for a set of documents.
        Used for multi-document verification.
        """
        if not document_scores:
            return {
                "overall_score": 0,
                "decision": "reject",
                "documents_analyzed": 0,
            }
        
        # Use minimum score (weakest document)
        min_score = min(d.get("overall_score", 0) for d in document_scores)
        
        # Check for any rejections
        any_rejected = any(d.get("decision") == "reject" for d in document_scores)
        
        # Check for any requiring review
        any_review = any(d.get("decision") == "review" for d in document_scores)
        
        if any_rejected:
            decision = "reject"
        elif any_review:
            decision = "review"
        else:
            decision = "approve"
        
        return {
            "overall_score": min_score,
            "decision": decision,
            "documents_analyzed": len(document_scores),
            "individual_scores": document_scores,
        }
    
    def adjust_thresholds(
        self,
        document_type: str,
    ) -> None:
        """
        Adjust thresholds based on document type.
        Higher-risk documents have stricter thresholds.
        """
        high_risk_types = ["passport", "cnic", "bank_statement"]
        medium_risk_types = ["degree", "experience_letter"]
        
        if document_type in high_risk_types:
            self.auto_approve_threshold = 0.98
            self.auto_reject_threshold = 0.4
        elif document_type in medium_risk_types:
            self.auto_approve_threshold = 0.92
            self.auto_reject_threshold = 0.35
        else:
            self.auto_approve_threshold = 0.90
            self.auto_reject_threshold = 0.3


# Global confidence scorer instance
confidence_scorer = ConfidenceScorer()
