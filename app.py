import streamlit as st
import pandas as pd
from datetime import datetime
from gdrive import upload_to_drive

# Load or initialize data
@st.cache_data
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
        try:
            file_id = upload_to_drive("finance_data.csv", f"finance_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            st.success(f"Transaction Saved & Uploaded to Google Drive! File ID: {file_id}")
        except Exception as e:
            st.error(f"Failed to upload to Google Drive: {str(e)}")

elif choice == "View Data":
    st.subheader("Transaction Records")
    st.write(df)