import streamlit as st
import stripe
import re
import os
from dotenv import load_dotenv

# Load API Keys
load_dotenv()
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""
    st.session_state.balance = 0
    st.session_state.is_new_user = False

# User authentication system
def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Placeholder: Replace with real authentication
        if email == "test@atm.com" and password == "SecurePass123":
            st.session_state.logged_in = True
            st.session_state.email = email
            st.session_state.balance = 1000  # Placeholder balance
            st.success("Login successful!")
        else:
            st.error("Invalid credentials!")

def register():
    st.subheader("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if password == password_confirm:
            # Placeholder: Replace with real registration logic
            st.session_state.logged_in = True
            st.session_state.email = email
            st.session_state.balance = 0  # Starting balance is 0
            st.session_state.is_new_user = True
            st.success("Registration successful!")
        else:
            st.error("Passwords do not match!")

def deposit_money():
    st.subheader("Deposit Money")
    amount = st.number_input("Enter amount to deposit", min_value=1.0, step=1.0)
    if st.button("Deposit"):
        # Stripe Payment Link (Simulated Deposit)
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "ATM Deposit"},
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://your-app-url.com/success",
            cancel_url="https://your-app-url.com/cancel",
        )
        st.success("Deposit link generated! Complete payment: " + session.url)

def withdraw_money():
    st.subheader("Withdraw Money")
    amount = st.number_input("Enter amount to withdraw", min_value=1.0, step=1.0)
    if st.button("Withdraw"):
        if amount <= st.session_state.balance:
            st.session_state.balance -= amount
            st.success(f"Withdrawal successful! New balance: ${st.session_state.balance}")
        else:
            st.error("Insufficient balance!")

def transfer_money():
    st.subheader("Transfer Money")
    recipient_iban = st.text_input("Recipient IBAN Number")
    amount = st.number_input("Enter amount to transfer", min_value=1.0, step=1.0)
    
    # IBAN validation (example: length check, real validation should be more complex)
    if len(recipient_iban) < 15 or len(recipient_iban) > 34:
        st.error("Invalid IBAN number! Please check the IBAN format.")
        return

    if st.button("Transfer"):
        if amount <= st.session_state.balance:
            # Deduct the amount from sender's balance
            st.session_state.balance -= amount
            st.success(f"Transferred ${amount} to IBAN: {recipient_iban}!")
        else:
            st.error("Insufficient balance!")

# Main UI
st.title("🌍 Global ATM App")

if not st.session_state.logged_in:
    choice = st.radio("Choose an option", ["Login", "Register"])
    if choice == "Login":
        login()
    elif choice == "Register":
        register()
else:
    st.sidebar.write(f"Logged in as: {st.session_state.email}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.email = ""
        st.session_state.balance = 0
        st.session_state.is_new_user = False
        st.rerun()
    
    option = st.sidebar.radio("Select an action", ["Check Balance", "Deposit Money", "Withdraw Money", "Transfer Money"])
    if option == "Check Balance":
        st.info(f"Your current balance: ${st.session_state.balance}")
    elif option == "Deposit Money":
        deposit_money()
    elif option == "Withdraw Money":
        withdraw_money()
    elif option == "Transfer Money":
        transfer_money()
