import streamlit as st
import sqlite3

# Initialize Database
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            college TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add Student Details to Database
def add_student(name, email, phone, city, state, college):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, phone, city, state, college) VALUES (?, ?, ?, ?, ?, ?)",
            (name, email, phone, city, state, college)
        )
        conn.commit()
        conn.close()
        return True, "🎉 Student details saved successfully!"
    except sqlite3.IntegrityError:
        return False, "❌ Error saving details. Please try again."

# Main App
def main():
    # Header
    st.title("🎓 Student Information Form")

    # Create a form
    with st.form("student_info_form"):
        st.header("Enter Student Details")

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        city = st.text_input("City")
        state = st.text_input("State")
        college = st.text_input("College Name")

        # Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Check if all fields are filled
            if name and email and phone and city and state and college:
                # Add data to database
                success, message = add_student(name, email, phone, city, state, college)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("⚠️ Please fill out all fields!")

# Run the app
if __name__ == "__main__":
    init_db()
    main()
