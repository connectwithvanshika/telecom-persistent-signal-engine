import yaml
import pandas as pd

from anomaly_detector import AnomalyDetector


with open("config.yaml") as f:

    config = yaml.safe_load(f)

detector = AnomalyDetector(config)

df = pd.read_csv(config["input_file"])

results = df.apply(detector.detect, axis=1)

df[
    [
        "Anomaly",
        "Severity",
        "Rule",
        "Reason"
    ]
] = pd.DataFrame(results.tolist(), index=df.index)

df.to_csv(config["output_file"], index=False)

print("✅ Analysis Complete")
print(f"Output saved to {config['output_file']}")