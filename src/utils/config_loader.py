import yaml


class ConfigLoader:

    def __init__(self, path):

        self.path = path

    def load(self):

        with open(self.path, "r") as f:

            config = yaml.safe_load(f)

        return config