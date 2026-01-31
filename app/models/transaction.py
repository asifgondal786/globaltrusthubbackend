"""
Transaction Model
Model for payments and financial transactions.
"""

from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum


class TransactionType(str, PyEnum):
    """Types of transactions."""
    SUBSCRIPTION = "subscription"
    SERVICE_PAYMENT = "service_payment"
    PROMOTION = "promotion"
    REFUND = "refund"


class TransactionStatus(str, PyEnum):
    """Transaction status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentMethod(str, PyEnum):
    """Payment methods."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    JAZZCASH = "jazzcash"
    EASYPAISA = "easypaisa"
    PAYPAL = "paypal"
    STRIPE = "stripe"


class Transaction:
    """
    Transaction model for payments.
    
    Attributes:
        id: Unique transaction identifier
        user_id: User making payment
        
        # Transaction Details
        transaction_type: Type of transaction
        amount: Transaction amount
        currency: Currency code (USD, PKR, etc.)
        
        # Payment
        payment_method: Method of payment
        payment_gateway: Gateway used
        gateway_transaction_id: External gateway ID
        
        # Status
        status: Transaction status
        failure_reason: Reason for failure if applicable
        
        # Related Entities
        subscription_id: Related subscription if applicable
        service_id: Related service if applicable
        provider_id: Service provider ID if applicable
        
        # Metadata
        description: Transaction description
        receipt_url: URL to receipt/invoice
        
        # Timestamps
        created_at: Transaction initiation time
        completed_at: Completion timestamp
    """
    
    __tablename__ = "transactions"
    
    id: str = ""
    user_id: str = ""
    
    # Transaction Details
    transaction_type: TransactionType = TransactionType.SUBSCRIPTION
    amount: float = 0.0
    currency: str = "USD"
    
    # Payment
    payment_method: PaymentMethod = PaymentMethod.STRIPE
    payment_gateway: str = "stripe"
    gateway_transaction_id: Optional[str] = None
    
    # Status
    status: TransactionStatus = TransactionStatus.PENDING
    failure_reason: Optional[str] = None
    
    # Related Entities
    subscription_id: Optional[str] = None
    service_id: Optional[str] = None
    provider_id: Optional[str] = None
    
    # Metadata
    description: str = ""
    receipt_url: Optional[str] = None
    
    # Timestamps
    created_at: datetime = datetime.utcnow()
    completed_at: Optional[datetime] = None
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, amount={self.amount} {self.currency}, status={self.status})>"
    
    @property
    def is_successful(self) -> bool:
        """Check if transaction completed successfully."""
        return self.status == TransactionStatus.COMPLETED
    
    @property
    def is_refundable(self) -> bool:
        """Check if transaction can be refunded."""
        if not self.is_successful:
            return False
        # Allow refunds within 30 days
        if self.completed_at:
            days_since = (datetime.utcnow() - self.completed_at).days
            return days_since <= 30
        return False
