import pandas as pd


class AnomalyDetector:

    def __init__(self, config):
        self.config = config

    def detect(self, row):

        triggered_rules = []
        reasons = []

        # =====================================================
        # RULE-001 : Weak Coverage Anomaly (RSRP)
        # =====================================================
        if row["RSRP"] < -110:

            triggered_rules.append("RULE-001")

            reasons.append(
                f"RSRP is {row['RSRP']} dBm, which is below the acceptable threshold of -110 dBm, indicating weak radio coverage."
            )

        # =====================================================
        # RULE-002 : Radio Interference (SINR)
        # =====================================================
        if row["SINR"] < 0:

            triggered_rules.append("RULE-002")

            reasons.append(
                f"SINR is {row['SINR']} dB, which is below the acceptable threshold of 0 dB, indicating severe interference and degraded radio quality."
            )

        # =====================================================
        # RULE-003 : Poor Signal Quality (RSRQ)
        # =====================================================
        if row["RSRQ"] < -15:

            triggered_rules.append("RULE-003")

            reasons.append(
                f"RSRQ is {row['RSRQ']} dB, which is below the acceptable threshold of -15 dB, indicating poor signal quality."
            )

        # =====================================================
        # RULE-004 : High RSSI Noise
        # =====================================================
        if row["RSSI"] > -55:

            triggered_rules.append("RULE-004")

            reasons.append(
                f"RSSI is {row['RSSI']} dBm while SINR is only {row['SINR']} dB, indicating excessive radio interference."
            )

        # =====================================================
        # RULE-005 : Missing PCI
        # =====================================================
        if pd.isna(row["PCI"]):

            triggered_rules.append("RULE-005")

            reasons.append(
                "Physical Cell Identity (PCI) is missing, preventing proper identification of the serving LTE cell."
            )

        # =====================================================
        # RULE-006 : Missing CellID
        # =====================================================
        if pd.isna(row["CellID"]):

            triggered_rules.append("RULE-006")

            reasons.append(
                "Serving Cell ID is missing, preventing network cell identification."
            )

        # =====================================================
        # RULE-007 : Missing Connected Band
        # =====================================================
        if pd.isna(row["ConnectedBand"]):

            triggered_rules.append("RULE-007")

            reasons.append(
                "Connected LTE Band information is unavailable."
            )

        # =====================================================
        # RULE-008 : Invalid Network Mode
        # =====================================================
        if row["NetworkMode"] not in ["LTE", "NR"]:

            triggered_rules.append("RULE-008")

            reasons.append(
                f"Unexpected Network Mode '{row['NetworkMode']}' detected."
            )

        # =====================================================
        # NO ANOMALY
        # =====================================================

        if len(triggered_rules) == 0:

            return (
                "No Anomaly",
                "None",
                "-",
                "All measured radio parameters satisfy the configured telecom thresholds. No abnormal network behaviour was detected."
            )

        # =====================================================
        # SINGLE RULE DETECTED
        # =====================================================

        if len(triggered_rules) == 1:

            rule = triggered_rules[0]

            anomaly_map = {

                "RULE-001": "Weak Coverage Anomaly",

                "RULE-002": "Radio Interference Anomaly",

                "RULE-003": "Poor Signal Quality Anomaly",

                "RULE-004": "Radio Noise Anomaly",

                "RULE-005": "LTE Configuration Anomaly",

                "RULE-006": "Cell Identification Anomaly",

                "RULE-007": "Band Configuration Anomaly",

                "RULE-008": "Network Mode Anomaly"

            }

            severity_map = {

                "RULE-001": "High",

                "RULE-002": "High",

                "RULE-003": "Medium",

                "RULE-004": "Medium",

                "RULE-005": "Critical",

                "RULE-006": "Critical",

                "RULE-007": "Low",

                "RULE-008": "Low"

            }

            return (

                anomaly_map[rule],

                severity_map[rule],

                rule,

                reasons[0]

            )

        # =====================================================
        # MULTIPLE RULES DETECTED
        # =====================================================

        if len(triggered_rules) == 2:

            severity = "Medium"

        elif len(triggered_rules) == 3:

            severity = "High"

        else:

            severity = "Critical"

        reason = (
            "Multiple telecom rules were triggered simultaneously. "
            + " ".join(reasons)
        )

        return (

            "Critical Radio Signal Anomaly",

            severity,

            ", ".join(triggered_rules),

            reason

        )