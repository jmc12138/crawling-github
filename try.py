import utils
import yaml

with open('Token.yml','r',encoding='utf-8') as f:
    tokens = yaml.safe_load(f)

print(tokens)