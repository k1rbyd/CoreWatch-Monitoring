import psutil
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import datetime

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "System Monitoring Dashboard"

# Function to get system stats
def get_system_stats():
    memory = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent(interval=1)
    partitions = psutil.disk_partitions()
    battery = psutil.sensors_battery()
    network = psutil.net_io_counters()

    disk_usage = [
        {
            "device": p.device,
            "total": psutil.disk_usage(p.mountpoint).total / (1024 ** 3),
            "used": psutil.disk_usage(p.mountpoint).used / (1024 ** 3),
            "free": psutil.disk_usage(p.mountpoint).free / (1024 ** 3),
        }
        for p in partitions if psutil.disk_usage(p.mountpoint).total > 0
    ]

    # Get processes information
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        memory_info = proc.info['memory_info']
        memory_usage = memory_info.rss / (1024 ** 2) if memory_info else 0  # Check if memory_info is available
        processes.append({
            "pid": proc.info['pid'],
            "name": proc.info['name'],
            "memory": memory_usage,
        })

    return {
        "memory": {
            "total": memory.total / (1024 ** 3),
            "used": memory.used / (1024 ** 3),
            "free": memory.available / (1024 ** 3),
        },
        "cpu": cpu_usage,
        "disk": disk_usage,
        "battery": {"percent": battery.percent, "plugged": battery.power_plugged}
        if battery
        else None,
        "network": {"sent": network.bytes_sent / (1024 ** 2), "recv": network.bytes_recv / (1024 ** 2)},
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "processes": processes,
    }

# Layout of the dashboard
app.layout = html.Div(
    id="main-div",
    children=[
        html.Div(
            style={"textAlign": "center", "marginBottom": "30px"},
            children=[
                html.H1("Comprehensive System Monitoring Dashboard", id="title", style={"fontSize": "36px", "fontWeight": "bold"}),
                html.Div(
                    [
                        html.Label(
                            "Update Interval (seconds): ", 
                            style={
                                "marginRight": "10px", 
                                "fontSize": "18px",
                            }
                        ),
                        dcc.Dropdown(
                            id="interval-dropdown",
                            options=[
                                {"label": f"{i} seconds", "value": i * 1000}
                                for i in [1, 2, 5, 10, 15, 20, 30, 60]
                            ],
                            value=2000,
                            clearable=False,
                            style={
                                "width": "200px", 
                                "backgroundColor": "#333", 
                                "color": "#fff", 
                                "border": "1px solid #ccc", 
                                "borderRadius": "10px", 
                                "padding": "10px", 
                                "fontSize": "16px", 
                                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
                            },
                        )
                    ],
                    style={
                        "marginBottom": "10px", 
                        "justifyContent": "center", 
                        "alignItems": "center"
                    },
                ),
                html.Div(
                    [
                        html.Button(
                            id="mode-toggle",
                            n_clicks=0,
                            children=[
                                html.I(className="fa fa-sun", id="toggle-icon"),
                                " Toggle Mode",
                            ],
                            style={
                                "padding": "12px 25px",
                                "fontSize": "18px",
                                "cursor": "pointer",
                                "borderRadius": "5px",
                                "backgroundColor": "#FF5733", 
                                "color": "white",
                                "border": "none",
                                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                            },
                        ),
                    ],
                    style={"textAlign": "center", "marginBottom": "30px"},
                ),
            ],
        ),
        html.Div(id="last-updated", style={"textAlign": "center", "marginBottom": "30px", "fontSize": "18px", "fontStyle": "italic"}),
        html.Div(
            style={"display": "flex", "justifyContent": "space-around", "marginBottom": "30px"},
            children=[
                dcc.Graph(id="memory-usage", style={"width": "48%", "height": "300px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "border": "2px solid #ccc"}),
                dcc.Graph(id="cpu-usage", style={"width": "48%", "height": "300px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "border": "2px solid #ccc"}),
            ],
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "space-around", "marginBottom": "30px"},
            children=[
                dcc.Graph(id="disk-usage", style={"width": "48%", "height": "300px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "border": "2px solid #ccc"}),
                dcc.Graph(id="network-usage", style={"width": "48%", "height": "300px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "border": "2px solid #ccc"}),
            ],
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "space-around", "marginBottom": "30px"},
            children=[
                dcc.Graph(id="battery-status", style={"width": "48%", "height": "300px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "border": "2px solid #ccc"}),
                html.Div(id="process-table", style={"width": "48%", "overflowY": "scroll", "maxHeight": "300px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "border": "2px solid #ccc"}),
            ],
        ),
        dcc.Interval(id="interval-update", n_intervals=0),
    ],
)

# Callback to update the interval dynamically
@app.callback(
    Output("interval-update", "interval"),
    [Input("interval-dropdown", "value")]
)
def update_interval(interval_value):
    return interval_value

# Callback to toggle light/dark mode
@app.callback(
    [
        Output("main-div", "style"),
        Output("title", "style"),
        Output("toggle-icon", "className"),
        Output("interval-dropdown", "style"),
        Output("last-updated", "style"),
    ],
    [Input("mode-toggle", "n_clicks")]
)
def toggle_mode(n_clicks):
    is_dark = n_clicks % 2 == 1
    main_style = {
        "backgroundColor": "#333" if is_dark else "#f4f4f4",
        "color": "#f4f4f4" if is_dark else "#333",
        "padding": "20px",
    }
    title_style = {"textAlign": "center", "color": "#f4f4f4" if is_dark else "#333"}
    toggle_icon = "fa fa-moon" if is_dark else "fa fa-sun"
    
    dropdown_style = {
        "backgroundColor": "#fff", 
        "color": "#000" , 
        "border": "1px solid #ccc" if not is_dark else "1px solid #333"
    }
    
    last_updated_style = {"textAlign": "center", "color": "#f4f4f4" if is_dark else "#333", "fontStyle": "italic"}
    
    return main_style, title_style, toggle_icon, dropdown_style, last_updated_style

# Callback to update system stats
@app.callback(
    [
        Output("memory-usage", "figure"),
        Output("cpu-usage", "figure"),
        Output("disk-usage", "figure"),
        Output("network-usage", "figure"),
        Output("battery-status", "figure"),
        Output("process-table", "children"),
        Output("last-updated", "children"),
    ],
    [Input("interval-update", "n_intervals")]
)
def update_dashboard(n):
    stats = get_system_stats()

    # Memory Usage Graph
    memory_data = go.Figure(
        go.Bar(
            x=["Total", "Used"],
            y=[stats["memory"]["total"], stats["memory"]["used"]],
            marker={"color": ["#4CAF50", "#FF5733"]},
        )
    )
    memory_data.update_layout(title="Memory Usage (GB)", showlegend=False)

    # CPU Usage Graph
    cpu_data = go.Figure(
        go.Indicator(
            mode="gauge+number", value=stats["cpu"], title={"text": "CPU Usage (%)"},
            gauge={"axis": {"range": [None, 100]}, "bar": {"color": "#FF5733"}},
        )
    )

    # Disk Usage Graph
    disk_data = go.Figure(
        go.Bar(
            x=[d['total'] - d["used"] for d in stats["disk"]],
            y=[d['device'] for d in stats["disk"]],
            name="Free Space",
            orientation="h",
            marker={"color": "#4CAF50"},
            hovertemplate="%{x} GB Free<br>%{y}<extra></extra>",
        )
    )

    disk_data.add_trace(
        go.Bar(
            x=[d["used"] for d in stats["disk"]],
            y=[d['device'] for d in stats["disk"]],
            name="Occupied Space",
            orientation="h",
            marker={"color": "#FF5733"},
            hovertemplate="%{x} GB Occupied<br>%{y}<extra></extra>",
        )
    )

    disk_data.update_layout(
        title="Disk Usage (GB)",
        showlegend=True,
        barmode="stack",  # Stack the bars horizontally
        xaxis={"title": "Storage (GB)", "range": [0, max(d['total'] for d in stats["disk"])]},
        yaxis={"title": "Device"},
    )
    # Network Usage Graph
    network_data = go.Figure(
        go.Bar(
            x=["Sent", "Received"],
            y=[stats["network"]["sent"], stats["network"]["recv"]],
            marker={"color": ["#FF5733","#4CAF50"]},
        )
    )
    network_data.update_layout(title="Network Usage (MB)", showlegend=False)

    # Battery Status Graph
    battery_data = go.Figure(
        go.Indicator(
            mode="gauge+number", value=stats["battery"]["percent"], title={"text": "Battery (%)"},
            gauge={"axis": {"range": [None, 100]}, "bar": {"color": "#4CAF50" if stats["battery"]["plugged"] else "#FF5733"}},
        )
    )

    # Process Table
    process_rows = [html.Tr([html.Td(proc["name"]), html.Td(f"{proc['memory']:.2f} MB")]) for proc in stats["processes"]]
    process_table = html.Table(
        [html.Thead(html.Tr([html.Th("Process Name"), html.Th("Memory Usage (MB)")])), html.Tbody(process_rows)],
        style={"width": "100%", "border": "1px solid #ccc", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"},
    )

    # Last Updated Time
    last_updated = f"Last Updated: {stats['time']}"

    return memory_data, cpu_data, disk_data, network_data, battery_data, process_table, last_updated

if __name__ == "__main__":
    app.run_server(debug=True)