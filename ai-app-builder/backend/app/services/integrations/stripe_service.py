from typing import Dict, Any, Optional
import stripe
from ....core.config import settings

class StripeService:
    """
    Service for handling Stripe payment integrations.
    Supports payment processing, subscriptions, and webhooks.
    """
    
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    
    async def create_payment_intent(
        self, 
        amount: int, 
        currency: str = "usd",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe PaymentIntent for processing payments.
        
        Args:
            amount: Amount in smallest currency unit (e.g., cents for USD)
            currency: Three-letter ISO currency code
            metadata: Additional metadata for the payment
            
        Returns:
            Dict containing payment intent details
        """
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata or {}
            )
            return {
                "success": True,
                "payment_intent_id": payment_intent.id,
                "client_secret": payment_intent.client_secret,
                "status": payment_intent.status
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "stripe_error"
            }
    
    async def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe customer.
        
        Args:
            email: Customer email address
            name: Customer name
            metadata: Additional metadata
            
        Returns:
            Dict containing customer details
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {}
            )
            return {
                "success": True,
                "customer_id": customer.id,
                "email": customer.email,
                "name": customer.name
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "stripe_error"
            }
    
    async def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a subscription for a customer.
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            metadata: Additional metadata
            
        Returns:
            Dict containing subscription details
        """
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                metadata=metadata or {}
            )
            return {
                "success": True,
                "subscription_id": subscription.id,
                "status": subscription.status,
                "current_period_end": subscription.current_period_end
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "stripe_error"
            }
    
    def construct_webhook_event(self, payload: str, sig_header: str) -> Optional[Dict[str, Any]]:
        """
        Construct a Stripe webhook event for processing.
        
        Args:
            payload: Webhook payload
            sig_header: Signature header from the request
            
        Returns:
            Dict containing event data or None if invalid
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            return {
                "success": True,
                "event_id": event.id,
                "event_type": event.type,
                "data": event.data
            }
        except ValueError as e:
            # Invalid payload
            return {
                "success": False,
                "error": "Invalid payload",
                "error_type": "value_error"
            }
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return {
                "success": False,
                "error": "Invalid signature",
                "error_type": "signature_error"
            }
    
    async def refund_payment(
        self,
        payment_intent_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Refund a payment.
        
        Args:
            payment_intent_id: ID of the payment to refund
            amount: Amount to refund (optional, defaults to full amount)
            reason: Reason for refund (optional)
            
        Returns:
            Dict containing refund details
        """
        try:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=amount,
                reason=reason
            )
            return {
                "success": True,
                "refund_id": refund.id,
                "status": refund.status,
                "amount": refund.amount
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "stripe_error"
            }
    
    async def get_payment_methods(self, customer_id: str) -> Dict[str, Any]:
        """
        Get payment methods for a customer.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            Dict containing payment methods
        """
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card"
            )
            return {
                "success": True,
                "payment_methods": [
                    {
                        "id": pm.id,
                        "brand": pm.card.brand,
                        "last4": pm.card.last4,
                        "exp_month": pm.card.exp_month,
                        "exp_year": pm.card.exp_year
                    }
                    for pm in payment_methods.data
                ]
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "stripe_error"
            }