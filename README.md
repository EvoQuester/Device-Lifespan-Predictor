# 🛡️ Device Lifespan Predictor

A collaborative full-stack application developed to simulate a **Predictive Maintenance** workflow. This project combines **Statistical Modeling** with **Database Administration (DBA)** to monitor hardware health and log telemetry for audit.

## 👥 The Collaboration
This project was built as a joint effort to simulate a real-world cross-functional environment:
*   **Statistics Major:** Developed the weighted linear decay algorithm and three-tier risk classification logic.
*   **Database Administrator (DBA):** Engineered the PostgreSQL backend, managed data persistence, and implemented administrative "Export" and "Reset" functionalities.

## 🚀 Key Features
*   **Real-time Prediction:** Adjust temperature and RPM to see instant lifespan estimates.
*   **3-Tier Risk Assessment:** Visual feedback for **Healthy (5+ years)**, **Warning (2-5 years)**, and **High-Risk (< 2 years)** states.
*   **PostgreSQL Integration:** Every calculation is logged to a relational database for long-term tracking.
*   **Data Portability:** Export full history as a `.txt` report directly from the UI.
*   **Admin Tools:** Integrated "Reset" functionality to manage database state via SQL `TRUNCATE` commands.

## 🛠️ Tech Stack
*   **Language:** Python 3
*   **UI Framework:** Streamlit
*   **Database:** PostgreSQL
*   **Driver:** Psycopg2

## ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Device-Lifespan-Predictor.git](https://github.com/YOUR_USERNAME/Device-Lifespan-Predictor.git)
   cd Device-Lifespan-Predictor

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

3. **Install Dependencies:**
   Ensure you have a `requirements.txt` file in your directory, then run:
   ```bash
   pip install -r requirements.txt

4. **Database Configuration:**
   * Open **pgAdmin** (or your preferred SQL client).
   * Create a new database named `hardware_project`.
   * Open the **Query Tool** and execute the following SQL to initialize the tracking table:
   ```sql
   CREATE TABLE device_logs (
       id SERIAL PRIMARY KEY,
       device_temp FLOAT,
       device_speed FLOAT,
       predicted_lifespan_years FLOAT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

5. **Run the Application:**
   Launch the dashboard with the following command:
   ```bash
   streamlit run app.py   
