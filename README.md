# Telecom Persistent Signal Engine

Rule-based telecom anomaly detection system.

## Implemented Rule

✔ Persistent Poor Signal

## Rule

RSRP < -110 dBm

AND

SINR < 0 dB

for 3 consecutive measurements.

## Input

telemetry.csv

## Output

anomaly_report.csv