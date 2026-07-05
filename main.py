from pathlib import Path

import pandas as pd
import yaml

from anomaly_detector import AnomalyDetector


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file)


def read_input_chunks(config):
    input_settings = config["input"]

    return pd.read_csv(
        input_settings["file_path"],
        compression=input_settings["compression"],
        sep=input_settings["separator"],
        chunksize=input_settings["chunk_size"],
        nrows=input_settings.get("max_rows"),
        low_memory=False,
    )


def clean_chunk(data, config):
    monitored_columns = list(config["monitored_columns"].values())

    # Some exported telemetry files repeat the header as the first data row.
    for column_name in monitored_columns:
        data = data[data[column_name].astype(str) != column_name]

    return data


def write_report_chunk(data, output_path, include_header):
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    write_mode = "w" if include_header else "a"
    data.to_csv(output_file, index=False, mode=write_mode, header=include_header)


def main():
    config = load_config("config.yaml")
    detector = AnomalyDetector(config)

    total_rows = 0
    anomaly_count = 0
    include_header = True

    for chunk in read_input_chunks(config):
        clean_data = clean_chunk(chunk, config)
        anomaly_results = detector.detect_chunk(clean_data)
        anomaly_report = pd.concat(
            [
                clean_data.reset_index(drop=True),
                anomaly_results.reset_index(drop=True),
            ],
            axis=1,
        )

        write_report_chunk(
            anomaly_report,
            config["output"]["file_path"],
            include_header,
        )

        total_rows += len(anomaly_report)
        anomaly_count += (anomaly_report["Status"] == "Anomaly").sum()
        include_header = False

    normal_count = total_rows - anomaly_count

    print("Persistent Signal Anomaly analysis complete.")
    print(f"Rows processed: {total_rows}")
    print(f"Anomalies found: {anomaly_count}")
    print(f"Normal rows: {normal_count}")
    print(f"Report saved to: {config['output']['file_path']}")


if __name__ == "__main__":
    main()
