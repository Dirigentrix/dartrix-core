# DARTRIX Core

DARTRIX Core is a lightweight Python implementation of the 108 Hz resonance kernel, WolfGuardian deterministic safety gates, and Lampa Alladyna (AladdinLamp) operator pipeline.

## Quick start

```python
from dartrix_core import AladdinLamp, Intent

output, gate = AladdinLamp().operate("Hello", Intent.SUPPORT)
print(output, gate.decision)
```

## Development

```bash
pip install -r requirements.txt
pytest
```

The project is intentionally deterministic and dependency-light. See `docs/` for architecture, operators, and safety details.
