import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText

def send_confirmation_email(receiver_email, patient_name):

    sender_email = "YOUR_GMAIL@gmail.com"
    sender_password = "YOUR_APP_PASSWORD"

    subject = "Appointment Confirmation"

    body = f"""
Hello {patient_name},

Your appointment has been successfully booked at
Sri Sankara Vision Care.

Thank you.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

# Page Settings
st.set_page_config(
    page_title="Sri Sankara Vision Care",
    page_icon="👁️",
    layout="wide"
)

# Header
st.sidebar.title("🔐 Admin Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

admin_logged_in = False

if username == "admin" and password == "eyeclinic123":
    admin_logged_in = True
    st.sidebar.success("Login Successful")
elif username or password:
    st.sidebar.error("Invalid Username or Password")


st.title("👁️ Sri Sankara Vision Care")
st.subheader("Complete Eye Care Solutions")

# About Clinic
st.header("About Us")

st.write("""
Sri Sankara Vision Care provides comprehensive eye care services
with modern diagnostic facilities and personalized treatment.

Our mission is to protect and improve your vision through
quality eye care and patient-centered services.
""")

# Doctor Details
st.header("👨‍⚕️ Doctor Information")

st.write("""
**Dr. Y. Veera**

**Specialization:** Ophthalmologist

Experienced in diagnosis and treatment of various eye diseases,
vision correction, cataract management, and routine eye examinations.
""")

# Services
st.header("🩺 Our Services")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - Eye Checkup
    - Vision Testing
    - Cataract Screening
    - Eye Infection Treatment
    """)

with col2:
    st.markdown("""
    - Spectacle Consultation
    - Glaucoma Screening
    - Diabetic Eye Checkup
    - General Eye Care
    """)

# Working Hours
st.header("🕒 Working Hours")

st.info("""
Sunday to Saturday

9:00 AM to 11:30 PM
""")

# Appointment Booking
st.header("📅 Book Appointment")

name = st.text_input("Patient Name", key="name")

phone = st.text_input("Phone Number", key="phone")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120, key="age")
    


appointment_date = st.date_input("Appointment Date", key="appointment_date")

problem = st.text_area(" Problem", key="problem")

if st.button("Book Appointment"):

    data = {
        "Name": [name],
        "Phone": [phone],
        "Age": [age],
        "Appointment Date": [appointment_date],
        "Problem": [problem]
    }

    df = pd.DataFrame(data)

    file_name = "appointments.csv"

    if os.path.exists(file_name):
        df.to_csv(file_name, mode="a", header=False, index=False)
    else:
        df.to_csv(file_name, index=False)

    st.success("Appointment Saved Successfully!")
    send_confirmation_email,(name)
st.success("Confirmation Email Sent!")

# Contact Information
st.header("📞 Contact Us") 

st.write("""
📍 Sri Surya Complex, Shabul Bazar, Bandar Road, Challapalli

📞 7793927222

✉️ srisankaravisioncare@gmail.com
""")

email= st.text_input("Email Address")

# Footer
st.markdown("---")
st.write("© 2026 Sri Sankara Vision Care. All Rights Reserved.")


st.header("📋 View All Appointments")
st.header("🔍 Search Patient")

search_name = st.text_input("Enter Patient Name", key="search_patient_name")

if st.button("Search"):

    if os.path.exists("appointments.csv"):

        df = pd.read_csv("appointments.csv")

        result = df[df["Name"].str.contains(search_name, case=False, na=False)]

        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("Patient not found.")

    else:
        st.warning("No appointment records found.")

        st.header("🗑️ Delete Appointment")

delete_name = st.text_input("Enter Patient Name to Delete", key="delete_patient_name")



if os.path.exists("appointments.csv"):

        df = pd.read_csv("appointments.csv")

        df = df[df["Name"] != delete_name]

        df.to_csv("appointments.csv", index=False)

        st.success("Appointment deleted successfully!")

else:
        st.warning("No appointment records found.")

if admin_logged_in:


    #view all appointments
    st.header("Admin Dashboard")
   
if st.button("Show Appointments"):

    if os.path.exists("appointments.csv"):

      df= pd.read_csv("appointments.csv")

    st.metric("Total Appointments", len(df))

    #view all appointments
    st.subheader("All Appointments")
    #Download Button
    st.dataframe(df)



# Download Button
    st.download_button(label="Download Appointments CSV",
    data=df.to_csv(index=False),
    file_name="appointments.csv",
    mime="text/csv"
)
else:
    st.warning("No appointment records found.")
    #Search patient
if search_name:

    result = df[df["Name"].str.contains(search_name, case=False, na=False)]

    st.dataframe(result)



#Delete Patient
st.subheader("Delete Appointment")

if st.button("Delete Appointment"):
            
            df = df[df["Name"] != delete_name]

            df.to_csv("appointments.csv", index=False)

            st.success("Appointment deleted successfully!") 

else:
   st.warning("No appointment records found.")
   if search_name:

    result = df[
        df["Name"].str.contains(
            search_name,
            case=False,
            na=False
        )
    ]

    if not result.empty:
        st.dataframe(result)
    else:
        st.warning("Patient not found.")   
# Delete Appointment
st.subheader("🗑️ Delete Appointment")

delete_name = st.text_input("Enter Patient Name to Delete")

if st.button("Delete Appointmnent"):
        if not df.empty and delete_name:

            df = pd.read_csv("appointments.csv")

            df = df[df["Name"] != delete_name]

            df.to_csv("appointments.csv", index=False)

            st.success("Appointment deleted Successfully!")
            
else:
            st.warning("No appointment records found.")

#Generate appointmnent ID

file_name = "appointments.csv"

if os.path.exists(file_name):

        old_df = pd.read_csv(file_name)

        appointment_id = "APT" + str(1000 + len(old_df) + 1)

else:

        appointment_id = "APT1001"

    # Patient Data
data = {
        "Appointment ID": [appointment_id],
        "Name": [name],
        "Phone": [phone],
        "Age": [age],
        "Appointment Date": [appointment_date],
        "Problem": [problem]
    }

df = pd.DataFrame(data)

    # Save to CSV
if os.path.exists(file_name):

        df.to_csv(
            file_name,
            mode="a",
            header=False,
            index=False
        )

else:

        df.to_csv(
            file_name,
            index=False
        )

    # Success Messages
st.success("Appointment deleted Successfully!")
st.success(f"Your Appointment ID is: {appointment_id}")

    # Display Appointment Details
st.write("Appointment ID:", appointment_id)
st.write("Patient Name:", name)
st.write("Phone Number:", phone)
st.write("Age:", age)
st.write("Appointment Date:", appointment_date)
st.write("Problem:", problem)