"""Read local configuration without executing it or changing process variables."""
import os
from pathlib import Path
import re
import unicodedata


def normalize_model_text(text):
    """Use one explicit Unicode policy for model inputs; keep source records intact."""
    return unicodedata.normalize('NFC', text)


def read_settings():
    """Prefer cwd's env/.env, then the source project; process values win."""
    values = {}
    roots = (Path.cwd(), Path(__file__).resolve().parents[2])
    path = next((root / name for root in roots for name in ('env', '.env')
                 if (root / name).is_file()), None)
    if path is not None:
        for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = re.fullmatch(r'(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)', line)
            if not match:
                raise ValueError(f'Invalid configuration in {path.name}, line {number}')
            key, value = match.groups()
            if value.startswith(('"', "'")):
                quoted = re.fullmatch(r"(['\"])(.*?)\1\s*(?:#.*)?", value)
                if not quoted:
                    raise ValueError(f'Invalid configuration in {path.name}, line {number}')
                value = quoted.group(2)
            else:
                value = re.split(r'\s+#', value, maxsplit=1)[0].rstrip()
            values[key] = value
    # Resolve aliases within each layer so a process region beats either file spelling.
    file_region = values.get('AWS_REGION') or values.get('AWS_DEFAULT_REGION')
    values.update(os.environ)
    region = os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION') or file_region
    if region:
        values['AWS_REGION'] = region
    return values
