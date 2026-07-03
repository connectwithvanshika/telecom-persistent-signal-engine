from src.utils.config_loader import ConfigLoader
from src.utils.data_loader import DataLoader
from src.core.rule_engine import RuleEngine


def main():

    config = ConfigLoader("config/config.yaml").load()

    df = DataLoader(config["input_file"]).load()

    engine = RuleEngine(config)

    result = engine.run(df)

    result.to_csv(config["output_file"], index=False)

    print(result[[
        "DEVICE_ID",
        "Anomaly",
        "Severity",
        "Rule Triggered",
        "Reason"
    ]].head(20))


if __name__ == "__main__":
    main()