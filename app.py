import streamlit as st
import pandas as pd
import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )
    
#=========== PAGE CONFIGURATION ==============
st.set_page_config(
    page_title="Sri Sankara Vision Care",
    page_icon="👁️",
    layout="wide"
)
#=========== HEADER LOGO AND TITLE ==============
st.title("👁️ Sri Sankara Vision Care")
st.subheader("Complete Eye Care Solutions")

st.header("🏥 About Clinic")
st.write("""
Sri Sankara Vision Care provides advanced eye care solutions including diagnosis,
treatment and preventive care using modern equipment.
""")

# -----------------------------
# DOCTOR PROFILE
# -----------------------------
st.header("👨‍⚕️ Doctor Profile")
st.subheader("Dr. Y. Veera")
st.write("Specialization: Ophthalmologist")
st.write("Experience: 10+ years in eye care")

# -----------------------------
# SERVICES
# -----------------------------
st.header("🩺 Services")
st.write("""
✔ Eye Checkup  
✔ Vision Testing  
✔ Cataract Screening  
✔ Glass Prescription  
✔ Diabetic Eye Care  
✔ Emergency Eye Care  
""")

# -----------------------------
# WORKING HOURS
# -----------------------------
st.header("🕒 Working Hours")
st.info("""
Sunday - Saturday: 9:00 AM to 11:30 PM  
Sunday: Emergency Only
""")

# -----------------------------
# CONTACT INFO
# -----------------------------
st.header("📞 Contact Information")
st.write("📍 Sri Surya Complex, Shabul Bazar, Bandar Road, Challapalli")
st.write("📱 7793927222")
st.write("📧 srisankaravisioncare@gmail.com")


st.sidebar.title("🔐 Admin Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

admin_logged_in = False

if username == "admin" and password == "eyeclinic123":
    admin_logged_in = True
    st.sidebar.success("Login Successful")
elif username or password:
    st.sidebar.error("Invalid Username or Password")
    

st.write("Admin Logged In:", admin_logged_in)

# Test Database Connection
try:
    conn = get_connection()
    st.success("✅ MySQL Connected Successfully!")
    conn.close()
except Exception as e:
    st.error(f"❌ Database Connection Failed: {e}")
st.header("📅 Book Appointment")

name = st.text_input("Patient Name")
phone = st.text_input("Phone Number")
age = st.number_input("Age", min_value=1, max_value=120)
appointment_date = st.date_input("Appointment Date")
problem = st.text_area("Eye Problem")
if st.button("Book Appointment"):
   if not name or not phone or not age or not appointment_date or not problem:
        st.warning("Please fill in all the fields.")
   else:
        # Insert appointment into the database
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM appointments")
        count = cursor.fetchone()[0]

        appointment_id = "APT" + str(1001 + count)

        sql = """
        INSERT INTO appointments
        (appointment_id, name, phone, age, appointment_date, problem)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
        appointment_id,
        name,
        phone,
        age,
        appointment_date,
        problem
    )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        st.success("✅ Appointment Booked Successfully!")
        st.success(f"Appointment ID: {appointment_id}")

# -----------------------------
# Admin Dashboard
# -----------------------------
if admin_logged_in:

    st.header("📊 Admin Dashboard")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()

    st.metric("Total Appointments", len(appointments))

    if appointments:
        import pandas as pd

        df = pd.DataFrame(
            appointments,
            columns=[
                "ID",
                "Appointment ID",
                "Name",
                "Phone",
                "Age",
                "Appointment Date",
                "Problem"
            ]
        )

        st.dataframe(df)
    st.subheader("🔍 Search Patient")

    search_name = st.text_input("Enter Patient Name")

    if st.button("Search Patient"):

       conn = get_connection()
       cursor = conn.cursor()

       cursor.execute(
         "SELECT * FROM appointments WHERE name LIKE %s",
        ("%" + search_name + "%",),
       st.success("Database Connected Successfully 🚀") 
     )

       result = cursor.fetchall()

       cursor.close()
       conn.close()

       if result:
        search_df = pd.DataFrame(
            result,
            columns=[
                "ID",
                "Appointment ID",
                "Name",
                "Phone",
                "Age",
                "Appointment Date",
                "Problem"
            ]
        )

        st.dataframe(search_df)

    else:
        st.warning("No appointment records found.") 
    
    st.subheader("🗑️ Delete Appointment")

    delete_id = st.text_input("Enter Appointment ID to Delete")

    if st.button("Delete Appointment"):

       if delete_id:

          conn = get_connection()
          cursor = conn.cursor()

          cursor.execute(
            "DELETE FROM appointments WHERE appointment_id = %s",
            (delete_id,)
         )

          conn.commit()

          if cursor.rowcount > 0:
            st.success("✅ Appointment deleted successfully!")
          else:
            st.warning("❌ Appointment ID not found.")

          cursor.close()
          conn.close()

    else:
        st.warning("Please enter an Appointment ID.")    

    st.subheader("✏️ Update Appointment")

update_id = st.text_input("Enter Appointment ID to Update")

new_phone = st.text_input("New Phone Number")

new_problem = st.text_area("New Eye Problem")

if st.button("Update Appointment"):

    if update_id and new_phone and new_problem:

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        UPDATE appointments
        SET phone=%s, problem=%s
        WHERE appointment_id=%s
        """

        values = (
            new_phone,
            new_problem,
            update_id
        )

        cursor.execute(sql, values)
        conn.commit()

        if cursor.rowcount > 0:
            st.success("✅ Appointment Updated Successfully!")
        else:
            st.warning("❌ Appointment ID not found.")

        cursor.close()
        conn.close()

    else:
        st.warning("Please fill all the fields.")
    st.subheader("📥 Download Appointments")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM appointments")
appointments = cursor.fetchall()

cursor.close()
conn.close()

if appointments:

    download_df = pd.DataFrame(
        appointments,
        columns=[
            "ID",
            "Appointment ID",
            "Name",
            "Phone",
            "Age",
            "Appointment Date",
            "Problem"
        ]
    )

    csv = download_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="appointments.csv",
        mime="text/csv"
    )