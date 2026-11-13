
<div align="center">
MarineSense
Marine Motion & Sensor Monitoring Dashboard

A Python-based prototype for simulating, processing, visualising, and monitoring marine motion data.





</div>
Table of Contents

    1. Project Overview
    2. Objectives
    3. System Capabilities
    4. Sensor Model and Data
    5. System Architecture
    6. Monitoring and Alert Logic
    7. Technology Stack
    8. Project Structure
    9. Installation and Execution
    10. Using the Dashboard
    11. Data Export
    12. Design Considerations
    13. Current Limitations
    14. Potential Future Development
    15. Disclaimer and Intended Use

1. Project Overview

MarineSense is a Python prototype that demonstrates how marine motion and sensor measurements can be collected, represented, monitored, and presented through a web-based dashboard.

The application simulates a vessel's motion-related measurements, maintains a rolling history of generated readings, visualises changes over time, and evaluates selected measurements against configurable warning thresholds. The dashboard is built with Streamlit, while Pandas is used to organise the readings and Plotly provides interactive time-series visualisations.

The project is intended to demonstrate a small end-to-end data application: from generating structured measurements to presenting operationally relevant information in a human-readable interface.

    Data integrity statement: MarineSense currently uses generated demonstration data. It does not receive measurements from physical sensors, vessel systems, or an external data service.

2. Objectives

The project has the following technical objectives:

    Sensor-data modelling — represent marine motion measurements in a consistent, structured format.
    Time-series processing — maintain and transform a chronological collection of readings.
    Operational visualisation — make changes in motion-related measurements visible through interactive charts and summary metrics.
    Threshold-based monitoring — demonstrate how configurable rules can identify values that exceed illustrative limits.
    Data accessibility — allow users to inspect the underlying readings and export the recorded history as CSV.
    Interactive operation — provide manual and automatic simulation controls through a browser-based interface.

These objectives describe the scope of the prototype; they should not be interpreted as evidence of integration with production maritime infrastructure.
3. System Capabilities
Capability	Implementation
Sensor-data simulation	Generates fictional, continuously varying measurements
Historical data	Initial history of 60 readings, with timestamps spaced one minute apart
Live demonstration	Optional automatic generation of a new reading every three seconds
Manual updates	Generates a new reading on user request
Vessel selection	Selects between fictional demonstration vessel names
KPI overview	Displays the latest roll, pitch, heave, and acceleration values
Time-series visualisation	Interactive Plotly charts for motion and measurement trends
Warning evaluation	Checks roll angle and acceleration against user-defined thresholds
Raw-data inspection	Displays the recorded readings in a tabular view
CSV export	Downloads the available sensor history
Session persistence	Uses Streamlit Session State to retain data during application reruns
Dashboard design

The interface is organised around a monitoring workflow:

    Context: selected demonstration vessel and latest update time.
    Status: a high-level indication of whether the latest reading exceeds the configured demonstration limits.
    Measurements: summary cards for the latest motion values.
    Trends: time-series charts for examining changes over the retained history.
    Warnings: a table containing triggered rules, current values, and suggested verification actions.
    Data access: a raw-data table and CSV export control.

4. Sensor Model and Data

MarineSense generates a structured record containing the following fields:
Field	Description	Demonstration unit
timestamp	Date and time associated with the reading	Local application time
roll	Side-to-side rotational angle	Degrees (°)
pitch	Forward/backward rotational angle	Degrees (°)
heave	Vertical displacement	Metres (m)
accel	Acceleration measurement	Metres per second squared (m/s²)
temperature	Simulated temperature measurement	Degrees Celsius (°C)

The simulation uses bounded changes relative to the preceding reading for roll, pitch, heave, and acceleration. This creates a degree of continuity between successive values rather than generating every measurement independently.

A low-probability event is also introduced during generation to make threshold warnings observable during a demonstration. The resulting values are fictional and are not calibrated against a particular vessel, sensor, sea state, or measurement standard.
Historical data generation

On initial application setup, MarineSense creates a history containing 60 readings. Their timestamps are assigned at one-minute intervals. Subsequent manual or automatic updates append new readings to the history.

The application retains the most recent 180 readings when new data is appended. This provides a bounded in-memory history for the dashboard session.
5. System Architecture

The current implementation follows a lightweight, single-application architecture.
Sensor SimulationStructured MeasurementRecordPandas DataFrameStreamlit Session StateMonitoring and ThresholdEvaluationPlotly Time-Series VisualisationStatus and Warning InterfaceInteractive DashboardRaw-Data TableCSV Export
Processing workflow

    Generation: the simulation function creates a new measurement using the previous reading as its starting point.
    Structuring: the generated values are represented as a record with a timestamp and named measurement fields.
    Storage: Pandas DataFrames organise the readings, while Streamlit Session State retains the current history across application reruns.
    Evaluation: the latest roll and acceleration values are compared with the thresholds selected in the sidebar.
    Presentation: Streamlit renders the current status, KPI cards, warning information, and data tables.
    Visualisation: Plotly renders interactive charts from the retained time-series data.
    Export: the recorded history can be serialised as CSV for further inspection.

Architectural scope

The current version keeps the simulation, data handling, monitoring rules, and user interface in app.py. This is appropriate for a compact demonstration, but it is not a modular production architecture. A future implementation could separate these responsibilities into dedicated modules and introduce a persistent data store and a defined sensor-ingestion interface.
6. Monitoring and Alert Logic

MarineSense demonstrates a basic rule-based monitoring approach. The application evaluates the latest reading against two configurable thresholds.
Roll-angle rule

The absolute value of roll is evaluated so that positive and negative rotations are treated consistently:
∣roll∣≥roll threshold
∣roll∣≥roll threshold

The default demonstration threshold is 12°. The sidebar allows the user to select a value between 5° and 18°.
Acceleration rule

The latest acceleration measurement is evaluated using:
acceleration≥acceleration threshold
acceleration≥acceleration threshold

The default demonstration threshold is 1.5 m/s². The sidebar allows the user to select a value between 0.5 and 2.5 m/s².
Status evaluation

The overall demonstration status is set to a warning state when either rule is triggered:
Warning=Roll warning∨Acceleration warning
Warning=Roll warning∨Acceleration warning

When neither condition is met, the interface displays a nominal status.

Triggered rules are listed in the alarm panel with the measurement name, current value, rule that was evaluated, and a suggested verification action.

Important: these thresholds are illustrative software parameters. They are not maritime operating limits, engineering recommendations, or validated safety criteria. The application evaluates the latest reading; it does not implement a certified alarm-management process, persistence logic, or safety response workflow.
7. Technology Stack
Technology	Role in MarineSense
Python	Application logic and sensor-data simulation
Streamlit	Browser-based dashboard and interactive controls
Pandas	Tabular data structures, history management, and CSV preparation
Plotly	Interactive time-series charts
CSS	Custom dashboard styling
Dependencies

The project declares the following minimum package versions in requirements.txt:
streamlit >= 1.36
pandas >= 2.0
plotly >= 5.20

Python 3.10 or newer is required.
8. Project Structure
MarineSense/
├── app.py                 # Dashboard, simulation, data handling and warning logic
├── requirements.txt       # Python package dependencies
├── run_dashboard.bat      # Windows quick-start script
├── PRESENTATION_NOTES.md  # Supporting presentation notes
└── README.md              # Project documentation
9. Installation and Execution
Prerequisites

    Python 3.10 or newer
    Git (if cloning the repository)
    A terminal or code editor, such as Visual Studio Code
    An internet connection for the initial dependency installation

9.1 Clone the repository
git clone https://github.com/Starley-iggy/MarineSense.git
cd MarineSense

Alternatively, download the repository as a ZIP archive and extract it locally.
9.2 Create a virtual environment

Windows (PowerShell):
py -m venv .venv
.\.venv\Scripts\Activate.ps1

macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

A virtual environment isolates the project's Python dependencies from other Python applications on the machine.
9.3 Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
9.4 Start the dashboard
python -m streamlit run app.py

Streamlit will display a local address in the terminal. Open that address in a browser; the default is usually:
http://localhost:8501
Windows quick start

On Windows, the included run_dashboard.bat script can be used to create the virtual environment if necessary, install the dependencies, and launch the dashboard.
10. Using the Dashboard

After launching the application:

    Select one of the fictional demonstration vessels in the sidebar.
    Review the current roll, pitch, heave, and acceleration values.
    Adjust the roll and acceleration thresholds to explore the warning behaviour.
    Select Generate new reading to append a single simulated measurement.
    Enable Live simulation to generate readings automatically at approximately three-second intervals.
    Inspect the charts to explore how the measurements change over time.
    Open the raw-data section to inspect the underlying records.
    Use the CSV export control to download the available history.

The dashboard is designed to make the data-processing and monitoring workflow observable during a demonstration.
11. Data Export

The application provides a CSV export of the current in-memory sensor history.

The exported file is named:
marinesense_sensor_history.csv

The export contains the measurement fields and timestamps represented in the application's history. It can be opened in spreadsheet software or used as input for additional analysis.

The current implementation does not write readings to a database or guarantee persistence after the Streamlit session or application process ends.
12. Design Considerations
Separation of measurement and presentation

The dashboard derives its displayed metrics, charts, and warning status from the generated measurement history. This makes the relationship between the underlying data and the user interface visible and easier to explain.
Bounded simulation values

The generator constrains several measurements to defined ranges. This keeps the demonstration data within predictable bounds and makes the interface easier to explore. These bounds are simulation parameters, not physical operating constraints.
Stateful interaction

Streamlit reruns the application in response to user interaction. Session State is therefore used to retain the sensor history, most recent reading, and live-simulation setting between reruns.
Bounded in-memory history

The history is limited to the latest 180 readings as new measurements are appended. This keeps the demonstration's working data set bounded, but it is not a substitute for durable storage or long-term time-series management.
Explicit treatment of uncertainty

A monitoring interface can make measurements easier to interpret, but a visual status indicator does not establish that a vessel or system is safe. Real-world use would require verified sensor sources, documented units, calibration, data-quality controls, domain-approved thresholds, and appropriate validation.
13. Current Limitations

MarineSense is a functional prototype, not a production maritime monitoring platform. Its current limitations include:

    Simulated input: no physical sensor, vessel network, API, or message broker is connected.
    In-memory storage: readings are not persisted in a database.
    Limited monitoring rules: only roll angle and acceleration are evaluated for warnings.
    Latest-reading evaluation: the warning logic does not analyse sustained conditions, rates of change, or historical alarm patterns.
    No sensor validation pipeline: missing, delayed, duplicated, out-of-range, or corrupted external measurements are not handled as a production ingestion concern.
    No authentication or authorisation: the application does not implement user accounts or role-based access.
    No operational deployment configuration: high availability, observability, backup, access control, and deployment hardening are outside the current scope.
    No safety certification: the application has not been assessed or approved for navigation, vessel operation, cargo decisions, or safety-critical use.

These limitations define the boundary between the current demonstration and a system that could be evaluated for operational use.
14. Potential Future Development

The following items are possible development directions. They are not implemented in the current version.
Area	Potential enhancement	Engineering value
Data ingestion	Integrate a documented sensor API or a verified data feed	Replace simulated input with traceable measurements
Messaging	Evaluate MQTT or another protocol once the source system is known	Support structured, near-real-time data delivery
Persistence	Introduce SQLite or a production-appropriate time-series database	Retain measurements beyond an application session
Architecture	Separate simulation, ingestion, processing, monitoring, and presentation	Improve maintainability and testability
Data quality	Add validation for missing, stale, duplicated, and implausible readings	Improve confidence in downstream processing
Monitoring	Add configurable rules, hysteresis, duration checks, and event history	Reduce simplistic threshold behaviour
Testing	Add unit and integration tests for data generation and monitoring rules	Verify expected behaviour and reduce regression risk
Observability	Introduce structured application logging and health checks	Improve troubleshooting and operational insight
Security	Add authentication, authorisation, and secure configuration	Establish controlled access
Deployment	Package and deploy the application using an agreed operational environment	Support repeatable deployment and maintenance

Any integration with real maritime systems would first require clarification of the available equipment, data formats, communication protocols, units, update rates, data ownership, and applicable operational requirements.
15. Disclaimer and Intended Use

MarineSense is an educational and portfolio prototype intended to demonstrate software development concepts related to sensor-data processing and visual monitoring.

All measurements, vessel names, and warning thresholds are used for demonstration purposes. The project is not connected to real vessel equipment and must not be used to make navigation, cargo, engineering, or safety decisions.

A real-world implementation would require, at minimum, verified data sources, documented measurement semantics and units, calibration and data-quality procedures, domain-expert review of monitoring rules, security controls, systematic testing, and an appropriate validation and approval process.
<div align="center">

MarineSense · Python · Streamlit · Pandas · Plotly

An exploratory software prototype for marine sensor-data visualisation and monitoring.
</div> 
