# 📡 Telecom Persistent Signal Engine

A rule-based telecom network anomaly detection engine that analyzes radio network telemetry and automatically identifies signal quality issues, radio interference, configuration problems, and missing network parameters.

The project processes LTE/5G telemetry logs and generates an anomaly report with severity levels, triggered rules, and detailed explanations for every detected issue.

---

# 🚀 Features

✅ Detects radio signal anomalies using configurable rule-based logic

✅ Processes raw telecom telemetry datasets

✅ Generates explainable anomaly reports

✅ Assigns severity levels to detected issues

✅ Identifies multiple simultaneous network problems

✅ Easily extendable with additional telecom rules

---

# 📂 Project Structure

```
telecom-persistent-signal-engine/

│
├── config/
│   ├── config.yaml
│   └── rules/
│       └── telecom_rules.yaml
│
├── data/
│   └── input/
│       └── telemetry.csv
│
├── output/
│   └── anomaly_report.csv
│
├── src/
│   ├── core/
│   │   ├── anomaly_detector.py
│   │   └── rule_engine.py
│   │
│   └── utils/
│       ├── config_loader.py
│       └── data_loader.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/connectwithvanshika/telecom-persistent-signal-engine.git

cd telecom-persistent-signal-engine
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

Place your telecom dataset inside

```
data/input/
```

Run

```bash
python main.py
```

The generated report will be saved in

```
output/anomaly_report.csv
```

---

# 📊 Dataset

The engine expects telecom radio measurements containing fields similar to:

- DEVICE_ID
- RSRP
- SINR
- RSSI
- RSRQ
- NetworkMode
- ConnectedBand
- CellID
- PCI
- Timestamp

---

# 🧠 Detection Rules

| Rule ID | Rule | Description |
|---------|------|-------------|
| RULE-001 | Weak Coverage | Detects extremely weak RSRP values |
| RULE-002 | Radio Interference | Detects poor SINR indicating severe interference |
| RULE-003 | Poor Signal Quality | Detects degraded RSRQ measurements |
| RULE-004 | Radio Noise | Detects excessive received signal strength with possible interference |
| RULE-005 | LTE Configuration | Detects missing PCI values |
| RULE-006 | Cell Identification | Detects missing Cell IDs |
| RULE-007 | Band Configuration | Detects missing LTE Band information |
| RULE-008 | Network Mode | Detects unexpected or unsupported network modes |

---

# 📈 Output Format

Each analyzed record contains the following information:

| Column | Description |
|---------|-------------|
| Anomaly | Type of anomaly detected |
| Severity | Low / Medium / High / Critical |
| Rule Triggered | Rule IDs responsible for detection |
| Reason | Human-readable explanation of the anomaly |

Example:

| Anomaly | Severity | Rule Triggered | Reason |
|----------|----------|----------------|--------|
| Radio Interference Anomaly | High | RULE-002 | SINR is -5 dB, which is below the acceptable threshold of 0 dB, indicating severe interference and degraded radio quality. |

---

# 📡 Radio Parameters Used

### RSRP (Reference Signal Received Power)

Measures received LTE reference signal strength.

Typical interpretation:

| RSRP |
|------|
| > -80 dBm Excellent |
| -80 to -90 Good |
| -90 to -100 Fair |
| -100 to -110 Poor |
| < -110 Very Poor |

---

### SINR (Signal to Interference plus Noise Ratio)

Measures radio quality.

| SINR |
|------|
| >20 Excellent |
| 13–20 Good |
| 0–13 Acceptable |
| <0 Severe Interference |

---

### RSRQ (Reference Signal Received Quality)

Measures signal quality.

| RSRQ |
|------|
| > -10 Good |
| -10 to -15 Fair |
| < -15 Poor |

---

### RSSI (Received Signal Strength Indicator)

Represents total received radio power including interference and background noise.

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- PyYAML

---

# Future Improvements

- Real-time streaming anomaly detection
- LTE/5G KPI dashboard
- Machine Learning-based anomaly detection
- Grafana integration
- Kafka support
- REST API
- Alerting system
- Time-series anomaly detection

---

# Example Workflow

```
Raw Telecom Telemetry
          │
          ▼
Data Loader
          │
          ▼
Configuration Loader
          │
          ▼
Rule Engine
          │
          ▼
Anomaly Detector
          │
          ▼
Severity Assignment
          │
          ▼
CSV Report Generation
```

---

# Why This Project?

Telecom operators continuously monitor radio network performance using Key Performance Indicators (KPIs). Poor radio conditions such as weak coverage, interference, degraded signal quality, or configuration issues can negatively impact user experience.

This project demonstrates how configurable rule-based analytics can automatically detect and explain such anomalies, providing interpretable insights without relying on machine learning models.

---

# Author

**Vanshika Yadav**

Computer Science & AI Undergraduate

Passionate about Artificial Intelligence, Data Science, Open Source, and Telecom Analytics.

GitHub:
https://github.com/connectwithvanshika

LinkedIn:
https://linkedin.com/in/connectwithvanshika