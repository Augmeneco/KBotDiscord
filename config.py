import json

class Config:
    names: list
    config: dict
    discord_token: str

    def __init__(self):
        self.config = json.loads(open('data/config.json', 'r', encoding='utf-8').read())

        self.names = self.config['names']
        self.discord_token = self.config['discord_token']

config = Config()
