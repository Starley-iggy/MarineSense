# MarineSense — Marine Sensor Monitoring Dashboard

A beginner-friendly Python portfolio project inspired by marine sensor and motion-monitoring systems.

## What it demonstrates

- Python functions and dictionaries
- Simulated time-series sensor data
- Pandas for storing and transforming readings
- Plotly for interactive charts
- Streamlit for a web-based dashboard
- Threshold-based warnings
- CSV export
- Session state and a simple live simulation

## Important limitation

**All data is simulated.** This project is not connected to real vessel equipment and is not a certified safety, navigation, or cargo-monitoring system. The example thresholds are for demonstrating software logic only.

## Requirements

- Python 3.10 or newer
- VS Code (recommended)
- Internet connection for the initial package installation

## Run in Windows / VS Code

1. Extract the ZIP file.
2. Open the `MarineSense_SIRI_Marine` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use the `run_dashboard.bat` file instead, or run the commands below without activating the environment.

6. Install packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. Start the dashboard:

   ```powershell
   python -m streamlit run app.py
   ```

8. Streamlit should open the dashboard in your browser. If it does not, open the local URL shown in the terminal (usually `http://localhost:8501`).

### Quick start

Double-click `run_dashboard.bat`. It creates `.venv` if needed, installs the dependencies, and starts the dashboard.

## Files

- `app.py` — dashboard, simulation, charts, and warning logic. It includes extensive comments.
- `requirements.txt` — Python packages.
- `run_dashboard.bat` — Windows quick-start script.
- `PRESENTATION_NOTES.md` — short speaking notes for a meeting.
- `README.md` — setup guide and project overview.

## Suggested 60-second explanation

> “I built MarineSense as a small Python prototype inspired by marine monitoring. Because I don't have access to real sensors, the app generates simulated roll, pitch, heave, and acceleration readings. Pandas stores the readings, Plotly visualizes trends, and Streamlit makes them available in an interactive dashboard. I added configurable thresholds to demonstrate how a warning system might work, plus raw-data inspection and CSV export. In a production environment, the simulator would be replaced by a verified sensor/API feed, and thresholds and safety behaviour would need to be defined and validated by domain experts.”

## Good next improvements

1. Save readings in SQLite.
2. Add unit tests for the warning rules.
3. Separate simulation, processing, and UI into different Python files.
4. Add a data-quality check for missing or implausible readings.
5. Add MQTT or an API only after confirming the real data source and protocol.
