import streamlit as st
import psycopg2

# --- THE "STATS MAJOR" LOGIC ---
def predict_lifespan(temp, speed):
    # A decay formula: lifespan starts at 5 years and drops as stress increases
    # Higher temp and speed = faster degradation
    calculation = 5.0 - (temp * 0.035) - (speed * 0.0004)
    result = round(max(0.5, calculation), 1) # Caps at 0.5 years for realism
    
    status = "Healthy: 2+ Years" if result >= 2.0 else "High Risk: < 2 Years"
    return result, status

# --- THE "DBA" LOGIC ---
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

# --- THE USER INTERFACE ---
st.set_page_config(page_title="Hardware Life Predictor", page_icon="🛡️")
st.title("🛡️ Device Lifespan Predictor")
st.markdown("Developed as a **DBA & Statistics** collaborative project.")

# Inputs
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
    else:
        st.success(health_status)
    
    # Save to PostgreSQL
    if log_prediction(temp_input, speed_input, years):
        st.caption("✅ Transaction successful: Result logged to PostgreSQL database.")