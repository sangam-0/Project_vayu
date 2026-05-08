# Project_vayu
IoT-based air quality monitoring system using Arduino and Python for real-time PM2.5, gas, temperature, and humidity tracking with an interactive dashboard.
# Air Quality Monitoring System using Arduino & Python

An IoT-based environmental monitoring system developed to measure:

- PM2.5
- Temperature
- Humidity
- Gas / CO₂ Levels

The project was inspired by observations of respiratory diseases such as COPD and asthma in Himalayan regions like Jumla, Nepal.

## Features

- Real-time monitoring dashboard
- Arduino sensor integration
- Live serial communication
- Interactive graphs using Dash & Plotly
- PM2.5 visualization
- Gas monitoring
- Environmental trend analysis

---

# Hardware Used

- Arduino Uno
- DHT11 Sensor
- MQ Gas Sensor
- PM2.5 Sensor
- Jumper wires
- Breadboard

---

# Software Stack

- Python
- Dash
- Plotly
- PySerial
- Arduino IDE

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/air-quality-monitoring-system.git
cd air-quality-monitoring-system
```

## Install Python Requirements

```bash
pip install -r requirements.txt
```

## Run Dashboard

```bash
python dashboard/app.py
```

Dashboard runs at:

```text
http://127.0.0.1:8050
```

---

# Arduino Upload

Open:

```text
arduino/air_quality_sensor.ino
```

Upload using Arduino IDE.

---

# Future Improvements

- GPS integration
- Cloud database
- Wireless sensor transmission
- Government-scale deployment
- Machine learning prediction
- Mobile application

---

# Motivation

This project was developed after observing respiratory health issues and environmental haze in Himalayan regions of Nepal. The aim is to create localized environmental monitoring systems that provide real ground-level data.

---

# Author
Sangam
