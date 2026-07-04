import pandas as pd


class AnomalyDetector:

    def __init__(self, config):

        self.rules = config["rules"]

    def detect(self, row):

        triggered = []
        reasons = []

        # -----------------------------
        # Weak Coverage
        # -----------------------------

        rule = self.rules["weak_coverage"]

        if rule["enabled"] and row["RSRP"] < rule["threshold"]:

            triggered.append(rule)

            reasons.append(
                f"RSRP ({row['RSRP']} dBm) is below {rule['threshold']} dBm."
            )

        # -----------------------------
        # Radio Interference
        # -----------------------------

        rule = self.rules["radio_interference"]

        if rule["enabled"] and row["SINR"] < rule["threshold"]:

            triggered.append(rule)

            reasons.append(
                f"SINR ({row['SINR']} dB) is below {rule['threshold']} dB."
            )

        # -----------------------------
        # Poor Signal Quality
        # -----------------------------

        rule = self.rules["poor_signal_quality"]

        if rule["enabled"] and row["RSRQ"] < rule["threshold"]:

            triggered.append(rule)

            reasons.append(
                f"RSRQ ({row['RSRQ']} dB) is below {rule['threshold']} dB."
            )

        # -----------------------------
        # Radio Noise
        # -----------------------------

        rule = self.rules["radio_noise"]

        if rule["enabled"] and row["RSSI"] > rule["threshold"]:

            triggered.append(rule)

            reasons.append(
                f"RSSI ({row['RSSI']} dBm) indicates excessive radio noise."
            )

        # -----------------------------
        # Missing PCI
        # -----------------------------

        rule = self.rules["missing_pci"]

        if rule["enabled"] and pd.isna(row["PCI"]):

            triggered.append(rule)

            reasons.append("PCI is missing.")

        # -----------------------------
        # Missing CellID
        # -----------------------------

        rule = self.rules["missing_cellid"]

        if rule["enabled"] and pd.isna(row["CellID"]):

            triggered.append(rule)

            reasons.append("CellID is missing.")

        # -----------------------------
        # Missing Connected Band
        # -----------------------------

        rule = self.rules["missing_band"]

        if rule["enabled"] and pd.isna(row["ConnectedBand"]):

            triggered.append(rule)

            reasons.append("Connected Band is missing.")

        # -----------------------------
        # Invalid Network Mode
        # -----------------------------

        rule = self.rules["invalid_network_mode"]

        if rule["enabled"] and row["NetworkMode"] not in rule["allowed"]:

            triggered.append(rule)

            reasons.append(
                f"Unexpected Network Mode '{row['NetworkMode']}'."
            )

        # --------------------------------
        # No anomaly
        # --------------------------------

        if len(triggered) == 0:

            return (
                "No Anomaly",
                "None",
                "-",
                "All telecom parameters are within configured thresholds."
            )

        # --------------------------------
        # Single anomaly
        # --------------------------------

        if len(triggered) == 1:

            r = triggered[0]

            return (

                r["anomaly_name"],

                r["severity"],

                "RULE-001",

                reasons[0]

            )

        # --------------------------------
        # Multiple anomalies
        # --------------------------------

        if len(triggered) == 2:

            severity = "Medium"

        elif len(triggered) == 3:

            severity = "High"

        else:

            severity = "Critical"

        return (

            "Critical Radio Signal Anomaly",

            severity,

            f"{len(triggered)} Rules Triggered",

            " ".join(reasons)

        )