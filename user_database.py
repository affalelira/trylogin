import streamlit as st
import pymysql

# Koneksi menggunakan streamlit secrets
def get_connection():
    return pymysql.connect(
        host=st.secrets["mysql"]["host"],       
        user=st.secrets["mysql"]["user"],       
        password=st.secrets["mysql"]["password"], 
        database=st.secrets["mysql"]["database"], 
        port=st.secrets["mysql"]["port"],        
        ssl={'ssl': {}},
        cursorclass=pymysql.cursors.DictCursor
    )

# CREATE
def add_data(name, age):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"❌ Error adding data: {e}")

# READ
def view_all_data():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        st.error(f"❌ Error reading data: {e}")
        return []

# UPDATE
def update_data(id, name, age):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE users SET name=%s, age=%s WHERE id=%s", (name, age, id))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"❌ Error updating data: {e}")

# DELETE
def delete_data(id):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id=%s", (id,))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"❌ Error deleting data: {e}")

# --- UI STYLING ---
st.set_page_config(page_title="CRUD Aiven + Streamlit", page_icon="🗃️", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        padding: 20px;
    }
    .box {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗂️ Data Management Dashboard")

menu = st.sidebar.radio("📋 Menu", ["Add", "View", "Update", "Delete"])

with st.container():
    st.markdown(f"<div class='box'>", unsafe_allow_html=True)

    if menu == "Add":
        st.subheader("➕ Add New User")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        if st.button("Add User"):
            add_data(name, age)
            st.success("✅ Data added successfully!")
            st.rerun()

    elif menu == "View":
        st.subheader("📄 View All Users")
        data = view_all_data()
        if data:
            st.table(data)
        else:
            st.info("No data found.")

    elif menu == "Update":
        st.subheader("✏️ Update User")
        id = st.number_input("User ID", min_value=1)
        name = st.text_input("New Name")
        age = st.number_input("New Age", min_value=0)
        if st.button("Update User"):
            update_data(id, name, age)
            st.success("✅ Data updated!")
            st.rerun()

    elif menu == "Delete":
        st.subheader("🗑️ Delete User")
        id = st.number_input("User ID", min_value=1)
        if st.button("Delete User"):
            delete_data(id)
            st.success("🧹 Data deleted!")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
