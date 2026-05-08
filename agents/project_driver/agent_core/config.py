from pathlib import Path
import yaml


def load_project_config(name: str = 'devx2'):
    base = Path(__file__).resolve().parent.parent
    path = base / 'projects' / f'{name}.yaml'

    with open(path, 'r') as f:
        return yaml.safe_load(f)
