import streamlit as st
import sqlite3
import pandas as pd


# Connect to SQLite Database
def connect_db():
    return sqlite3.connect("user_info.db")


# Function to create table if it doesn't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            city TEXT,
            state TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Function to add data into the database
def add_user_data(name, email, phone, city, state):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, email, phone, city, state)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, phone, city, state))
    conn.commit()
    conn.close()


# Function to fetch all users' data
def fetch_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    return data


# Main app logic
def main():
    st.title("User Information Form")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Submit Details", "Admin Page"])

    # Submit Details Page
    if page == "Submit Details":
        st.subheader("Student Form")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        city = st.text_input("City")
        state = st.text_input("State")
        college = st.text_input("College")

        if st.button("Submit"):
            if name and email and phone and city and state:
                add_user_data(name, email, phone, city, state)
                st.success("Data submitted successfully!")
            else:
                st.error("Please fill all the fields!")

    # Admin Page
    elif page == "Admin Page":
        st.subheader("Admin - View Submitted Data")

        # Admin Authentication (Optional)
        admin_password = st.text_input("Enter Admin Password", type="password")

        # Admin Login Logic
        if admin_password == "prasadclub":  # Replace with actual password logic
            st.success("Logged in as Admin")
            st.write("Admin Name: **Prasad Chowdary**")  # Display admin name

            data = fetch_data()

            if data:
                df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Phone", "City", "State"])
                st.dataframe(df)

                # Option to download data
                csv_data = df.to_csv(index=False)
                st.download_button("Download Database", csv_data, "user_data.csv")
            else:
                st.warning("No data found.")
        else:
            st.error("Invalid admin password!")


if __name__ == "__main__":
    create_table()
    main()
