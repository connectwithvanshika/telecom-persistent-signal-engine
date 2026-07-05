import re

import pandas as pd


class AnomalyDetector:
    """Simple rule-based detector for persistent telecom signal anomalies."""

    def __init__(self, config):
        self.rules = config["rules"]
        self.column_mapping = config["monitored_columns"]
        self.normal_reason = config["normal_reason"]

    def detect(self, row):
        """Return the anomaly decision fields for one telemetry row."""
        sinr = self._read_number(row, "Q")
        rssi = self._read_number(row, "R")
        rsrq = self._read_number(row, "S")
        network_mode = self._read_text(row, "T")
        timestamp = self._read_text(row, "U")

        rule_checks = [
            self._check_persistent_radio_degradation(sinr, rssi, rsrq),
            self._check_severe_interference(sinr, rsrq),
            self._check_excessive_noise(rssi, sinr),
            self._check_poor_signal_quality(rsrq, sinr),
            self._check_invalid_measurement(sinr, rssi, rsrq, network_mode, timestamp),
        ]

        triggered_rules = [rule for rule in rule_checks if rule is not None]

        if not triggered_rules:
            return {
                "Status": "Normal",
                "Anomaly_Name": "None",
                "Severity": "None",
                "Triggered_Rule": "None",
                "Reason": self.normal_reason,
            }

        highest_priority_rule = sorted(
            triggered_rules,
            key=lambda rule: self._severity_rank(rule["severity"]),
            reverse=True,
        )[0]

        return {
            "Status": "Anomaly",
            "Anomaly_Name": highest_priority_rule["anomaly_name"],
            "Severity": highest_priority_rule["severity"],
            "Triggered_Rule": highest_priority_rule["id"],
            "Reason": highest_priority_rule["reason"],
        }

    def detect_chunk(self, data):
        """Return anomaly decision columns for a pandas DataFrame chunk."""
        sinr = self._number_series(data, "Q")
        rssi = self._number_series(data, "R")
        rsrq = self._number_series(data, "S")
        network_mode = self._text_series(data, "T")
        timestamp = self._text_series(data, "U")

        results = pd.DataFrame(index=data.index)
        results["Status"] = "Normal"
        results["Anomaly_Name"] = "None"
        results["Severity"] = "None"
        results["Triggered_Rule"] = "None"
        results["Reason"] = self.normal_reason

        invalid_measurement = (
            sinr.isna()
            | rssi.isna()
            | rsrq.isna()
            | (network_mode == "")
            | (timestamp == "")
        )
        self._apply_chunk_result(
            results,
            invalid_measurement,
            self.rules["invalid_measurement"],
            "One or more monitored values in columns Q to U is missing or cannot be read.",
        )

        poor_quality_rule = self.rules["poor_signal_quality"]
        poor_quality = (
            rsrq.le(poor_quality_rule["rsrq_max"])
            & sinr.le(poor_quality_rule["sinr_max"])
        )
        self._apply_chunk_result(
            results,
            poor_quality,
            poor_quality_rule,
            "Column S/RSRQ and column Q/SINR are below the configured signal quality limits.",
        )

        noise_rule = self.rules["excessive_noise"]
        excessive_noise = (
            rssi.ge(noise_rule["rssi_min"])
            & sinr.le(noise_rule["sinr_max"])
        )
        self._apply_chunk_result(
            results,
            excessive_noise,
            noise_rule,
            "Column R/RSSI is high while column Q/SINR is poor, suggesting noise or interference.",
        )

        interference_rule = self.rules["severe_interference"]
        severe_interference = (
            sinr.le(interference_rule["sinr_max"])
            & rsrq.le(interference_rule["rsrq_max"])
        )
        self._apply_chunk_result(
            results,
            severe_interference,
            interference_rule,
            "Column Q/SINR and column S/RSRQ are below acceptable limits, indicating sustained radio interference.",
        )

        degradation_rule = self.rules["persistent_radio_degradation"]
        persistent_degradation = (
            sinr.le(degradation_rule["sinr_max"])
            & rssi.ge(degradation_rule["rssi_min"])
            & rsrq.le(degradation_rule["rsrq_max"])
        )
        self._apply_chunk_result(
            results,
            persistent_degradation,
            degradation_rule,
            "Columns Q/SINR, R/RSSI, and S/RSRQ show poor quality, high received power, and degraded radio conditions together.",
        )

        return results

    def _check_persistent_radio_degradation(self, sinr, rssi, rsrq):
        rule = self.rules["persistent_radio_degradation"]

        if not rule["enabled"]:
            return None

        if (
            sinr is not None
            and rssi is not None
            and rsrq is not None
            and sinr <= rule["sinr_max"]
            and rssi >= rule["rssi_min"]
            and rsrq <= rule["rsrq_max"]
        ):
            return self._build_result(
                rule,
                (
                    f"Column Q/SINR is {sinr} dB, column R/RSSI is {rssi} dBm, "
                    f"and column S/RSRQ is {rsrq} dB. Weak quality, high received "
                    "power, and poor radio quality are happening together."
                ),
            )

        return None

    def _check_severe_interference(self, sinr, rsrq):
        rule = self.rules["severe_interference"]

        if not rule["enabled"]:
            return None

        if (
            sinr is not None
            and rsrq is not None
            and sinr <= rule["sinr_max"]
            and rsrq <= rule["rsrq_max"]
        ):
            return self._build_result(
                rule,
                (
                    f"Column Q/SINR is {sinr} dB and column S/RSRQ is {rsrq} dB. "
                    "Both values are below acceptable limits, which indicates "
                    "sustained radio interference."
                ),
            )

        return None

    def _check_excessive_noise(self, rssi, sinr):
        rule = self.rules["excessive_noise"]

        if not rule["enabled"]:
            return None

        if (
            rssi is not None
            and sinr is not None
            and rssi >= rule["rssi_min"]
            and sinr <= rule["sinr_max"]
        ):
            return self._build_result(
                rule,
                (
                    f"Column R/RSSI is {rssi} dBm while column Q/SINR is {sinr} dB. "
                    "The site is receiving strong total radio power, but the signal "
                    "quality is poor, suggesting noise or interference."
                ),
            )

        return None

    def _check_poor_signal_quality(self, rsrq, sinr):
        rule = self.rules["poor_signal_quality"]

        if not rule["enabled"]:
            return None

        if (
            rsrq is not None
            and sinr is not None
            and rsrq <= rule["rsrq_max"]
            and sinr <= rule["sinr_max"]
        ):
            return self._build_result(
                rule,
                (
                    f"Column S/RSRQ is {rsrq} dB and column Q/SINR is {sinr} dB. "
                    "The signal quality is below the configured threshold."
                ),
            )

        return None

    def _check_invalid_measurement(self, sinr, rssi, rsrq, network_mode, timestamp):
        rule = self.rules["invalid_measurement"]

        if not rule["enabled"]:
            return None

        missing_fields = []

        if sinr is None:
            missing_fields.append("Q/SINR")
        if rssi is None:
            missing_fields.append("R/RSSI")
        if rsrq is None:
            missing_fields.append("S/RSRQ")
        if not network_mode:
            missing_fields.append("T/SYS_SUB_MODE")
        if not timestamp:
            missing_fields.append("U/TIMESTAMP")

        if missing_fields:
            return self._build_result(
                rule,
                (
                    "The row has missing or invalid monitored values in "
                    f"{', '.join(missing_fields)}, so the signal condition cannot "
                    "be trusted."
                ),
            )

        return None

    def _build_result(self, rule, reason):
        return {
            "id": rule["id"],
            "anomaly_name": rule["anomaly_name"],
            "severity": rule["severity"],
            "reason": reason,
        }

    def _read_number(self, row, column_letter):
        column_name = self.column_mapping[column_letter]
        raw_value = row.get(column_name)

        if pd.isna(raw_value):
            return None

        match = re.search(r"-?\d+(\.\d+)?", str(raw_value))

        if match is None:
            return None

        return float(match.group())

    def _number_series(self, data, column_letter):
        column_name = self.column_mapping[column_letter]

        return pd.to_numeric(
            data[column_name].astype(str).str.extract(r"(-?\d+(\.\d+)?)")[0],
            errors="coerce",
        )

    def _read_text(self, row, column_letter):
        column_name = self.column_mapping[column_letter]
        raw_value = row.get(column_name)

        if pd.isna(raw_value):
            return ""

        text_value = str(raw_value).strip()

        if text_value == column_name:
            return ""

        return text_value

    def _text_series(self, data, column_letter):
        column_name = self.column_mapping[column_letter]

        return (
            data[column_name]
            .fillna("")
            .astype(str)
            .str.strip()
            .replace(column_name, "")
        )

    def _apply_chunk_result(self, results, mask, rule, reason):
        if not rule["enabled"]:
            return

        results.loc[mask, "Status"] = "Anomaly"
        results.loc[mask, "Anomaly_Name"] = rule["anomaly_name"]
        results.loc[mask, "Severity"] = rule["severity"]
        results.loc[mask, "Triggered_Rule"] = rule["id"]
        results.loc[mask, "Reason"] = reason

    def _severity_rank(self, severity):
        severity_order = {"Low": 1, "Medium": 2, "High": 3}
        return severity_order.get(severity, 0)
