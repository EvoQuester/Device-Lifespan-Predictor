1. Requirements
Install the necessary Python bridges:
pip install streamlit psycopg2

Create a database named hardware_project in pgAdmin and run this SQL:
CREATE TABLE device_logs (
    id SERIAL PRIMARY KEY,
    device_temp FLOAT,
    device_speed FLOAT,
    predicted_lifespan_years FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

3. Launch
Run the app locally:
streamlit run app.py
