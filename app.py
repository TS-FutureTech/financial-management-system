import streamlit as st
import pandas as pd
from datetime import datetime
import json
from gdrive import upload_to_drive

# Create or Load Data
def load_data():
    try:
        return pd.read_csv("finance_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Description"])

df = load_data()

# Streamlit App UI
st.title("📊 Financial Management System")

menu = ["Home", "Record Transaction", "View Data"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.write("Welcome to the Financial Management System!")
    st.write("Manage Donations, Expenditures, and Assets efficiently.")

elif choice == "Record Transaction":
    st.subheader("Add a New Transaction")
    date = st.date_input("Transaction Date", datetime.today())
    trans_type = st.selectbox("Transaction Type", ["Donation", "Expenditure", "Asset"])
    category = st.text_input("Category (e.g., Rent, Food, Charity)")
    amount = st.number_input("Amount (PKR)", min_value=0.0, step=100.0)
    description = st.text_area("Description")

    if st.button("Save Transaction"):
        new_data = pd.DataFrame([[date, trans_type, category, amount, description]],
                                columns=["Date", "Type", "Category", "Amount", "Description"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv("finance_data.csv", index=False)
        upload_to_drive("finance_data.csv", "finance_data_backup.csv")
        st.success("Transaction Saved & Uploaded to Google Drive!")

elif choice == "View Data":
    st.subheader("Transaction Records")
    st.write(df)

