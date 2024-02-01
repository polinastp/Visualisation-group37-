# Visualization Tool 

## Overview
This README provides instructions on how to set up and run a visualization tool that analyzes soccer player data across various metrics such as shooting, defense, possession, and passing. The tool utilizes Python libraries including Pandas for data manipulation, Plotly for interactive visualizations, and Dash for web application development.

## Requirements
- Python 3.6 or higher
- Pandas
- Plotly
- Dash
- NumPy
- Matplotlib

## Installation
Ensure that Python 3.6 or higher is installed on your system. You can download it from [the official Python website](https://www.python.org/downloads/).

1. **Set up a virtual environment (optional but recommended):**
   - On Windows: `python -m venv venv`
   - On macOS/Linux: `python3 -m venv venv`

2. **Activate the virtual environment:**
   - On Windows: `.\venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. **Install required packages:**
   - `pip install pandas plotly dash numpy matplotlib`

## Data Preparation
Place the following datasets in a folder named `Dataset` within your project directory:
- `player_shooting.csv`
- `player_defense.csv`
- `player_possession.csv`
- `player_passing.csv`
- `WorldCupShootouts.csv`

Ensure that each dataset is correctly formatted and includes the appropriate columns as referenced in the provided code.

## Running the Tool
1. Navigate to the project directory in your terminal or command prompt.
2. Run the tool by executing: `python <name_of_your_script>.py`
   - Replace `<name_of_your_script>` with the filename of your Python script containing the visualization tool code.

## Using the Tool
Upon running the script, the Dash web server will start, and you should see a message indicating the URL to access the web application, typically `http://127.0.0.1:8050/`.

Open this URL in a web browser to interact with the visualization tool. The dashboard allows for dynamic selection of teams and players to compare various statistics through interactive charts and graphs.

## Features
- Radar charts comparing team statistics.
- Violin plots for visual comparison of selected attributes between two teams.
- Scatter plots showing successful shots per zone with a soccer field overlay.
- Bar charts comparing successful and unsuccessful shots per zone.

## Troubleshooting
- Ensure all datasets are correctly placed in the `Dataset` folder.
- Check for any missing or misspelled column names in the datasets.
- Verify that all required packages are installed.
- If the web application doesn't load, check the terminal for any error messages.

## Conclusion
This visualization tool provides insightful analyses for coaches, players, and soccer enthusiasts to explore player performance and team dynamics. For any questions or issues, please refer to the documentation of the respective Python libraries used or consult online forums for community support.
