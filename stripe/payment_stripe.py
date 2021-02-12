import stripe
# test API key
stripe.api_key = 'sk_test_51I7i27LkymEpeCOCyr09iG9R95ASUGWKOXvgpaD1P9xp6pUc1cqslsRft3YDe41ooeX0cZ0YnzYiagl710D5Jeld00eNIRoAYM'

stripePayment = stripe.PaymentIntent.create(
  amount=1000,
  currency='sgd',
  payment_method_types=['card'],
  receipt_email='jenny.rosen@example.com',
)

print(stripePayment)