
# System Monitoring Dashboard

This is a System Monitoring Dashboard built using Python, Dash, and Plotly. The dashboard provides real-time insights into various system statistics, including CPU, memory, disk usage, network activity, battery status, and processes. It also includes a toggle mode feature for light/dark mode.

## Features
	•	Real-time system monitoring: Displays system statistics such as CPU usage, memory usage, disk usage, network activity, and battery status.
	•	Process Monitoring: Displays a table of running processes with memory usage details.
	•	Interactive Visuals: Utilizes interactive plots to show system statistics in a visually appealing format.
	•	Light/Dark Mode Toggle: Toggle between light and dark themes for better user experience.
	•	Update Interval: Allows you to adjust the update interval of the dashboard.

## Technologies Used
	•	Dash: A web framework for building analytical web applications.
	•	Plotly: A graphing library for creating interactive plots and charts.
	•	psutil: A library for retrieving system and process information.
	•	Python: The core programming language used to develop the application.

## Installation

To get started with the project, follow these steps:
	
 1. Clone the repository
	
 		git clone https://github.com/yourusername/system-monitoring-dashboard.git
		cd system-monitoring-dashboard
	
2. Create a virtual environment (optional but recommended)
	
 		python -m venv venv
	
3. Activate the virtual environment
	
  •	On Windows:
  
		venv\Scripts\activate
	
•	On macOS/Linux:
	
		source venv/bin/activate
	
4. Install required dependencies
	
		pip install -r requirements.txt
	
	Here is the requirements.txt:
	
		dash==2.0.0
		psutil==5.8.0
		plotly==5.0.0
	
5. Run the application
	
	Once the dependencies are installed, you can run the application using the following command:
	
		python app.py
	
	The app will start a local server at http://127.0.0.1:8050/ by default.

## How It Works

1. System Stats Collection (get_system_stats function)
	
	The application retrieves system stats using the psutil library. It collects information such as:
		•	Memory Usage: Total, used, and free memory in gigabytes.
		•	CPU Usage: The percentage of CPU currently in use.
		•	Disk Usage: The storage status of all mounted partitions, showing both free and used space.
		•	Battery Status: Battery percentage and whether the system is plugged in.
		•	Network Usage: Data sent and received over the network in megabytes.
		•	Running Processes: A list of processes with their memory usage.
	
	The get_system_stats function organizes this data into a dictionary that is later used to update the dashboard’s visuals.
	
3. Dashboard Layout
	
	The dashboard consists of the following components:
		•	Title Section: Displays the title of the dashboard and an interval dropdown for setting the update frequency.
		•	System Stats Graphs:
		•	Memory Usage: A bar chart showing total and used memory.
		•	CPU Usage: A gauge chart showing the percentage of CPU usage.
		•	Disk Usage: A stacked bar chart showing free and used disk space for each partition.
		•	Network Usage: A bar chart showing the amount of data sent and received over the network.
		•	Battery Status: A gauge chart showing the current battery percentage.
		•	Process Table: A table listing the active processes and their memory usage.
		•	Last Updated: A label indicating the time when the stats were last updated.
	
4. Callbacks
	
	The application uses Dash callbacks to handle the real-time update of the dashboard:
		•	Update Interval: The interval-dropdown lets users choose the update frequency (1, 2, 5, 10, 15, 20, 30, 60 seconds).
		•	Light/Dark Mode Toggle: The button toggles between light and dark themes. The UI is dynamically updated based on the current mode.
		•	System Stats Update: Every time the interval elapses, the system stats are fetched again, and the graphs are updated.
	
5. Mode Toggle Feature
	
	The light/dark mode toggle allows users to switch between light and dark themes. This feature is achieved by changing the background color and text color of the entire layout, including individual components like the title, graphs, and dropdown menus.
	
6. Real-time Data Update
	
	The application automatically updates the dashboard at the selected interval (e.g., every 1, 2, 5, 10, 15, 20, 30, or 60 seconds). It uses Dash’s Interval component to periodically fetch new system stats and update the UI.
	
7. Graph Components
	
	The app uses Plotly for creating interactive graphs:
		•	Memory Usage: A bar chart with two bars representing total and used memory.
		•	CPU Usage: A gauge chart displaying the current CPU usage as a percentage.
		•	Disk Usage: A horizontal stacked bar chart displaying the free and used space for each mounted disk.
		•	Network Usage: A bar chart comparing the amount of data sent and received.
		•	Battery Status: A gauge chart displaying battery percentage and status.
	
8. Process Table
	
	The table displays a list of running processes with memory usage. It updates dynamically as the system stats change.
	
9. Last Updated Time
	
	The dashboard shows the last updated timestamp to inform the user when the data was last refreshed.

## Contributing

If you would like to contribute to the project, feel free to fork the repository, create a branch, and submit a pull request. Contributions are always welcome!

