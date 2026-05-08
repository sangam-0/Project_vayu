import time
import threading
import collections
import serial

import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# ================= CONFIG =================
SERIAL_PORT = "COM3"
BAUD_RATE = 9600
DEMO_MODE = False
MAX_POINTS = 40

# ================= DATA =================
buf = {
    "time": collections.deque(maxlen=MAX_POINTS),
    "temp": collections.deque(maxlen=MAX_POINTS),
    "hum": collections.deque(maxlen=MAX_POINTS),
    "gas": collections.deque(maxlen=MAX_POINTS),
    "pm": collections.deque(maxlen=MAX_POINTS),
}

latest = {"temp":0,"hum":0,"gas":0,"pm":0}
lock = threading.Lock()

# ================= DEMO DATA =================
def demo():
    import random, math
    t = time.time()
    return (
        25 + math.sin(t/5)*3,
        55 + math.sin(t/6)*7,
        300 + math.sin(t/4)*120,
        40 + math.sin(t/7)*25
    )

# ================= PUSH =================
def push(temp, hum, gas, pm):
    ts = time.strftime("%H:%M:%S")
    with lock:
        buf["time"].append(ts)
        buf["temp"].append(temp)
        buf["hum"].append(hum)
        buf["gas"].append(gas)
        buf["pm"].append(pm)
        latest.update({"temp":temp,"hum":hum,"gas":gas,"pm":pm})

# ================= SERIAL =================
def reader():
    if DEMO_MODE:
        while True:
            push(*demo())
            time.sleep(3)
    else:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)

            while True:
                line = ser.readline().decode(errors="ignore").strip()
                parts = line.split(",")

                if len(parts) == 4:
                    try:
                        push(float(parts[0]), float(parts[1]), int(parts[2]), int(parts[3]))
                    except:
                        pass
        except:
            print("Serial error → DEMO mode ON")
            while True:
                push(*demo())
                time.sleep(3)

threading.Thread(target=reader, daemon=True).start()

# ================= DASH APP =================
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# ================= GAUGE =================
def gauge(v, title, color, rng):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=v,
        title={"text": title, "font": {"size": 12}},  # ✅ FIXED
        gauge={"axis":{"range":rng},"bar":{"color":color}}
    )).update_layout(
        height=210,
        margin=dict(t=60,b=10,l=10,r=10)  # ✅ FIXED spacing
    )

# ================= SMALL GRAPH =================
def small(x, y, color, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, line=dict(color=color)))

    fig.update_layout(
        height=180,
        title=title,
        margin=dict(t=35,b=20,l=30,r=10),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="white", size=11)
    )
    return fig

# ================= LAYOUT =================
app.layout = html.Div(
    style={"padding":"12px","backgroundColor":"#0f172a"},
    children=[

    # ===== TITLE (FIXED GAP) =====
    html.H3(
        " Air Quality Monitoring Dashboard",
        style={
            "textAlign": "center",
            "color": "white",
            "marginBottom": "25px",  # ✅ FIXED
            "marginTop": "10px"
        }
    ),

    html.Div(id="live",
             style={"textAlign":"center","color":"#94a3b8","marginBottom":"10px"}),

    # ================= GAUGES =================
    dbc.Row([
        dbc.Col(dcc.Graph(id="g1", config={"displayModeBar":False}), md=3),
        dbc.Col(dcc.Graph(id="g2", config={"displayModeBar":False}), md=3),
        dbc.Col(dcc.Graph(id="g3", config={"displayModeBar":False}), md=3),
        dbc.Col(dcc.Graph(id="g4", config={"displayModeBar":False}), md=3),
    ], style={"marginBottom":"10px"}),

    # ================= SMALL GRAPHS =================
    dbc.Row([
        dbc.Col(dcc.Graph(id="t", config={"displayModeBar":False}), md=6),
        dbc.Col(dcc.Graph(id="h", config={"displayModeBar":False}), md=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="g", config={"displayModeBar":False}), md=6),
        dbc.Col(dcc.Graph(id="p", config={"displayModeBar":False}), md=6),
    ]),

    # ================= COMBINED =================
    dbc.Row([
        dbc.Col(dcc.Graph(id="all", config={"displayModeBar":False}), md=12),
    ]),

    dcc.Interval(id="i", interval=3000)
])

# ================= UPDATE =================
@app.callback(
    Output("g1","figure"),
    Output("g2","figure"),
    Output("g3","figure"),
    Output("g4","figure"),
    Output("t","figure"),
    Output("h","figure"),
    Output("g","figure"),
    Output("p","figure"),
    Output("all","figure"),
    Output("live","children"),
    Input("i","n_intervals")
)
def update(_):

    with lock:
        x = list(buf["time"])
        t = list(buf["temp"])
        h = list(buf["hum"])
        g = list(buf["gas"])
        p = list(buf["pm"])
        cur = latest.copy()

    # ===== GAUGES =====
    g1 = gauge(cur["temp"], "Temp °C", "red", [0,50])
    g2 = gauge(cur["hum"], "Humidity %", "blue", [0,100])
    g3 = gauge(cur["gas"], "Gas", "purple", [0,1023])
    g4 = gauge(cur["pm"], "PM2.5", "green", [0,200])

    # ===== SMALL GRAPHS =====
    t_g = small(x,t,"red","Temperature Trend")
    h_g = small(x,h,"blue","Humidity Trend")
    g_g = small(x,g,"purple","Gas Trend")
    p_g = small(x,p,"green","PM2.5 Trend")

    # ===== COMBINED =====
    allg = go.Figure()
    allg.add_trace(go.Scatter(x=x,y=t,name="Temp",line=dict(color="red")))
    allg.add_trace(go.Scatter(x=x,y=h,name="Hum",line=dict(color="blue")))
    allg.add_trace(go.Scatter(x=x,y=g,name="Gas",line=dict(color="purple")))
    allg.add_trace(go.Scatter(x=x,y=p,name="PM2.5",line=dict(color="green")))
    allg.update_layout(height=300, paper_bgcolor="#111827", plot_bgcolor="#111827")

    return (
        g1,g2,g3,g4,
        t_g,h_g,g_g,p_g,
        allg,
        f"T:{cur['temp']:.1f}°C | H:{cur['hum']:.1f}% | Gas:{cur['gas']} | PM2.5:{cur['pm']}"
    )

# ================= RUN =================
if __name__ == "__main__":
    print("Dashboard running → http://127.0.0.1:8050")
    app.run(debug=False)