from src.core.anomaly_detector import AnomalyDetector


class RuleEngine:

    def __init__(self, config):
        self.detector = AnomalyDetector(config)

    def run(self, dataframe):

        anomaly = []
        severity = []
        rules = []
        reasons = []

        for _, row in dataframe.iterrows():

            a, s, r, reason = self.detector.detect(row)

            anomaly.append(a)
            severity.append(s)
            rules.append(r)
            reasons.append(reason)

        dataframe["Anomaly"] = anomaly
        dataframe["Severity"] = severity
        dataframe["Rule Triggered"] = rules
        dataframe["Reason"] = reasons

        return dataframe