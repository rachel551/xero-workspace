import yaml
import os

def load_env_from_yaml(yaml_file, collection_name):
    """
    This function loads the environment variables from config file.
    It needs the file and collection names.
    """
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
        env_vars = config.get(collection_name, {})
        
        for key, value in env_vars.items():
            os.environ[key] = str(value)

