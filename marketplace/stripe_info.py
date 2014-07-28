import stripe

__author__ = 'WillieTran'


# secret_key = 'sk_test_eBoq5GKhL3wNB1PwDW8owedu' #Test secret key
# pub_key = 'pk_test_pWxm3wMH8P9Lvrp96uZp7nHK' #Test publishable key


#secret_key = 'sk_live_s3r94YyWefgseEYbzKspFtx4' #Live secret key
#pub_key = 'pk_live_UOChTX1somui4onsvUB0RWgR' #Live publishable key

# Set your secret key: remember to change this to your live secret key in production
# See your keys here https://dashboard.stripe.com/account
stripe.api_key = "sk_test_eBoq5GKhL3wNB1PwDW8owedu"

# Get the credit card details submitted by the form
token = request.POST['stripeToken']

# Create a Customer
customer = stripe.Customer.create(
    card=token,
    description="payinguser@example.com"
)

# Charge the Customer instead of the card
stripe.Charge.create(
    amount=1000, # in cents
    currency="usd",
    customer=customer.id
)

# Save the customer ID in your database so you can use it later
save_stripe_customer_id(user, customer.id)

# Later...
customer_id = get_stripe_customer_id(user)

stripe.Charge.create(
    amount=1500, # $15.00 this time
    currency="usd",
    customer=customer_id
)