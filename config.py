import yaml

with open('config.yaml', 'r', encoding='utf-8') as file:
    config_data = yaml.safe_load(file)
