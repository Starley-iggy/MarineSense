# Presentation notes — MarineSense

## 30-second intro
“I built MarineSense as a small Python prototype inspired by marine sensor monitoring. It uses simulated data, so I can demonstrate the software without claiming to connect to real vessel equipment.”

## How the app works
1. `generate_sensor_reading()` creates a fictional sensor reading.
2. Pandas stores the readings in a table.
3. Streamlit renders the dashboard and controls.
4. Plotly displays motion and acceleration trends.
5. The app compares the latest values with adjustable demo thresholds.
6. The user can inspect raw data and export it to CSV.

## Explain these terms
- **Roll:** side-to-side rotation of a vessel.
- **Pitch:** forward/backward rotation.
- **Heave:** vertical movement.
- **Time-series data:** measurements recorded over time.
- **Threshold:** a configured value used to decide whether to show a warning.
- **Streamlit:** a Python framework for quickly creating interactive data apps.
- **Plotly:** a library for interactive charts.
- **Pandas:** a Python library for working with tables of data.

## Questions you may get

**Why Python?**  
“It is quick to prototype with and has strong libraries for data processing and visualization.”

**Is the data real?**  
“No. It is simulated. I would need access to a documented data source and hardware/API details to connect real measurements.”

**What would you do next?**  
“I would add automated tests, store readings in a database, validate units and data quality, and then integrate a real data source only after confirming the system requirements.”

**How do you know the warning thresholds are correct?**  
“They are demonstration values only. Real thresholds must be specified and validated by qualified engineers using the actual system requirements.”

**What did you learn?**  
“I practiced the full flow from data generation to processing, visualization, user controls, and export. I also considered how to make the prototype transparent about its limitations.”

## Honest positioning
Describe this as a learning prototype, not a production system. If you did not write or understand a section fully, take time to read the comments and test it before presenting it.
