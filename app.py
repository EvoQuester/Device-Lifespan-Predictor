import streamlit as st
import psycopg2
from datetime import datetime

# --- THE "STATS MAJOR" LOGIC ---
def predict_lifespan(temp, speed):
    base_life = 8.0 
    calculation = base_life - (temp * 0.05) - (speed * 0.0006)
    result = round(max(0.5, calculation), 1)
    
    if result >= 5.0:
        status = "Healthy: 5+ Years"
    elif result >= 2.0:
        status = "Warning: 2-5 Years (Monitor Closely)"
    else:
        status = "High Risk: < 2 Years (Immediate Action)"
        
    return result, status

# --- THE "DBA" LOGIC: Saving Data ---
def log_prediction(t, s, r):
    try:
        conn = psycopg2.connect(
            dbname="hardware_project",
            user="postgres",
            password="postgres", 
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO device_logs (device_temp, device_speed, predicted_lifespan_years) VALUES (%s, %s, %s)",
            (t, s, r)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database Error: {e}")
        return False

# --- THE "DBA" LOGIC: Fetching Data ---
def get_history_as_text():
    try:
        conn = psycopg2.connect(dbname="hardware_project", user="postgres", password="postgres", host="localhost")
        cur = conn.cursor()
        cur.execute("SELECT id, device_temp, device_speed, predicted_lifespan_years, created_at FROM device_logs ORDER BY created_at DESC LIMIT 20")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        report = "🛡️ DEVICE HEALTH HISTORY REPORT\n"
        report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "="*50 + "\n\n"
        report += "ID | Temp(C) | Speed(RPM) | Lifespan(Yrs) | Date Logged\n"
        report += "-"*70 + "\n"
        for row in rows:
            report += f"{row[0]} | {row[1]}°C | {row[2]} RPM | {row[3]} Yrs | {row[4].strftime('%Y-%m-%d %H:%M')}\n"
        return report
    except Exception as e:
        return f"Error generating report: {e}"

# --- THE "DBA" LOGIC: Resetting the Table ---
def clear_database():
    try:
        conn = psycopg2.connect(dbname="hardware_project", user="postgres", password="postgres", host="localhost")
        cur = conn.cursor()
        # TRUNCATE is the pro way to wipe a table and reset IDs to 1
        cur.execute("TRUNCATE TABLE device_logs RESTART IDENTITY;")
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Reset Error: {e}")
        return False

# --- THE USER INTERFACE ---
st.set_page_config(page_title="Hardware Life Predictor", page_icon="🛡️")
st.title("🛡️ Device Lifespan Predictor")

# Input Section
st.subheader("Current Metrics")
col1, col2 = st.columns(2)
with col1:
    temp_input = st.slider("Operating Temp (°C)", 20, 110, 45)
with col2:
    speed_input = st.slider("Device Speed (RPM)", 500, 6000, 2500)

if st.button("Calculate Lifespan"):
    years, health_status = predict_lifespan(temp_input, speed_input)
    st.divider()
    st.header(f"Prediction: {years} Years Remaining")
    
    if "High Risk" in health_status:
        st.error(health_status)
    elif "Warning" in health_status:
        st.warning(health_status)
    else:
        st.success(health_status)
    
    if log_prediction(temp_input, speed_input, years):
        st.caption("✅ Transaction successful: Result logged to PostgreSQL database.")

# --- EXPORT & ADMIN SECTION ---
st.write("") 
st.write("") 
st.divider()

# Create two columns for Export and Reset
admin_col1, admin_col2 = st.columns(2)

with admin_col1:
    st.subheader("📊 Data Export")
    report_content = get_history_as_text()
    st.download_button(
        label="💾 Download History (.txt)",
        data=report_content,
        file_name="device_health_history.txt",
        mime="text/plain"
    )

with admin_col2:
    st.subheader("⚠️ Danger Zone")
    if st.button("🗑️ Reset Database"):
        if clear_database():
            st.success("Database wiped successfully. IDs reset to 1.")
            st.rerun() # Refresh app to update the download report