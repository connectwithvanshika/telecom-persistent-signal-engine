import re
import pandas as pd


class DataLoader:

    def __init__(self, path):

        self.path = path

    def clean_signal(self, value):

        if pd.isna(value):

            return None

        value = str(value)

        match = re.search(r'-?\d+\.?\d*', value)

        if match:

            return float(match.group())

        return None

    def load(self):

        df = pd.read_csv(self.path)

        signal_columns = [

            "RSRP",
            "SINR",
            "RSSI",
            "RSRQ"

        ]

        for col in signal_columns:

            if col in df.columns:

                df[col] = df[col].apply(self.clean_signal)

        return df