# Persistent Signal Anomaly

A small, beginner-friendly telecom rule engine that detects persistent signal anomalies from network telemetry.

This project does not use machine learning or deep learning. It uses clear threshold-based rules that resemble how a telecom engineer might manually inspect weak radio quality, interference, and noisy signal conditions.

## Project Structure

```text
telecom-persistent-signal-engine/
|
├── main.py
├── anomaly_detector.py
├── config.yaml
├── requirements.txt
├── README.md
|
├── data/
|   └── input/
|       └── Telemetry_X_ATP_last7days_20260622.csv.gz
|
└── output/
    └── anomaly_report.csv
```

## Columns Used

The input file is tab-delimited. The rule engine only uses Excel-style columns Q, R, S, T, and U from the dataset.

| Excel Column | Dataset Column | Meaning |
| --- | --- | --- |
| Q | SINR | Signal to interference plus noise ratio |
| R | RSSI | Total received radio signal power |
| S | RSRQ | Reference signal received quality |
| T | SYS_SUB_MODE | Radio access mode, such as LTE |
| U | TIMESTAMP | Measurement timestamp |

All original columns are kept in the final report.

## Detection Rules

Thresholds are stored in `config.yaml` so they can be changed without editing Python code.
The input is processed in chunks of 100,000 rows so large compressed telemetry files can be handled on a normal laptop.

| Rule ID | Anomaly Name | Severity | Logic |
| --- | --- | --- | --- |
| RULE-001 | Persistent Poor Signal | High | SINR is at or below 0 dB, RSSI is at or above -65 dBm, and RSRQ is at or below -12 dB. |
| RULE-002 | Sustained Radio Interference | High | SINR is at or below 0 dB and RSRQ is at or below -10 dB. |
| RULE-003 | Excessive Radio Noise | Medium | RSSI is at or above -60 dBm while SINR is at or below 3 dB. |
| RULE-004 | Poor Signal Quality | Medium | RSRQ is at or below -14 dB while SINR is at or below 8 dB. |
| RULE-005 | Invalid Signal Measurement | Low | One or more monitored values in columns Q to U is missing or cannot be read. |

## Sample Rule Explanations

| Status | Anomaly_Name | Severity | Triggered_Rule | Reason |
| --- | --- | --- | --- | --- |
| Anomaly | Persistent Poor Signal | High | RULE-001 | Column Q/SINR is -11 dB, column R/RSSI is -54 dBm, and column S/RSRQ is -14 dB. Weak quality, high received power, and poor radio quality are happening together. |
| Anomaly | Sustained Radio Interference | High | RULE-002 | Column Q/SINR is -2 dB and column S/RSRQ is -10 dB. Both values are below acceptable limits, which indicates sustained radio interference. |
| Normal | None | None | None | All monitored signal parameters are within acceptable limits. |

If multiple rules are triggered for the same row, the report keeps the highest-severity rule so each row has one clear decision.

## Output Columns

The generated report is saved to:

```text
output/anomaly_report.csv
```

The output contains all original input columns plus:

| Column | Description |
| --- | --- |
| Status | `Anomaly` or `Normal` |
| Anomaly_Name | Name of the detected anomaly |
| Severity | `Low`, `Medium`, `High`, or `None` |
| Triggered_Rule | Rule ID such as `RULE-001`, or `None` |
| Reason | Human-readable explanation for the decision |

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Make sure the input file exists at:

```text
data/input/Telemetry_X_ATP_last7days_20260622.csv.gz
```

Then run:

```bash
python main.py
```

The script prints a small summary and writes the report to `output/anomaly_report.csv`.

## Workflow

```text
Input telemetry CSV.GZ
        |
        v
Read config.yaml
        |
        v
Load tab-delimited data with pandas
        |
        v
Apply AnomalyDetector rules
        |
        v
Add explainable output columns
        |
        v
Write output/anomaly_report.csv
```

## Technologies

- Python
- pandas
- PyYAML

## Author

Vanshika Yadav
