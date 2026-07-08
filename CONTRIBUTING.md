# Adding a New Data Source (Connector)

The TUI auto-discovers connectors from the `hermes/connectors/` directory tree.  
You just need to create the right folder structure and implement `Connector` + `metadata()`.

---

## Step 1 — Pick Your IDs

From `hermes/registry.py`, find your source in `_STATIC_SOURCES`. Note its `id`, `category`, and `subcategory`.  
If it's a brand-new source not listed, add an entry there first.

---

## Step 2 — Create Directory Structure

```
hermes/connectors/<category>/<subcategory>/<id>/
├── __init__.py
├── connector.py       # Required: your Connector subclass
├── auth.py            # Optional (split if auth logic is non-trivial)
├── fetch.py           # Optional
├── export.py          # Optional
├── transformer.py     # Optional
└── validate.py        # Optional
```

Example for FRED (Macroeconomic, Finance):

```
hermes/connectors/finance/Macroeconomic/fred/
├── __init__.py
└── connector.py
```

> **Case conventions** — directory names match the `id` field: lowercase, underscores.

---

## Step 3 — Write `__init__.py`

```python
from hermes.connectors.<category>.<subcategory>.<id>.connector import MyConnector

__all__ = ["MyConnector"]
```

---

## Step 4 — Write the Connector Class

```python
from hermes.connectors.base.base_model import Connector
from typing import Any


class MyConnector(Connector):

    @classmethod
    def metadata(cls) -> dict:
        """
        Return source metadata.
        The TUI uses this to generate the parameter form and credential screen.
        """
        return {
            "id": "my_source_id",
            "name": "My Display Name",
            "category": "Finance & Economics",
            "subcategory": "Macroeconomic",
            "description": "Short description of what this source provides.",
            "credentials": [
                {"key": "api_key", "label": "API Key"},
                # or {"key": "email", "label": "Email"},
                # or {"key": "password", "label": "Password"},
            ],
            "parameters": [
                {"name": "symbol", "type": "string", "label": "Stock Symbol", "default": "AAPL"},
                {"name": "limit", "type": "integer", "label": "Max Records", "default": 100},
                # type can be: "string", "integer", "number", "date"
            ],
            "outputs": ["CSV", "JSON", "PostgreSQL"],
        }

    def authenticate(self) -> bool:
        ...

    def validate_credentials(self) -> bool:
        ...

    def fetch(self) -> list[dict[str, Any]]:
        ...

    def validate(self) -> list[dict[str, Any]]:
        ...

    def transform(self) -> Any:
        ...

    def export(self, data: list[dict[str, Any]], destination: str) -> None:
        ...

    def health_check(self) -> dict:
        ...
```

---

## Step 5 — Run

```bash
uv run python hermes.py
```

The TUI will:
1. Walk `hermes/connectors/` looking for `__init__.py` files
2. Import each one and look for non-abstract `Connector` subclasses
3. Call `.metadata()` and register the source
4. Replace the catalog stub with the full metadata

Your source will appear in:
- **Data Sources** → click through → full parameter form
- **Credentials** → click through → credential inputs generated from metadata

---

## Metadata Fields Reference

| Field | Required | Description |
|---|---|---|
| `id` | Yes | Matches the static catalog entry. Must be unique. |
| `name` | Yes | Display name in the UI |
| `category` | Yes | Top-level category name (must match `_STATIC_SOURCES`) |
| `subcategory` | Yes | Second-level grouping (must match `_STATIC_SOURCES`) |
| `description` | No | Shown on the source detail screen |
| `credentials` | No | List of `{"key": str, "label": str}`. Each generates a password-masked input. |
| `parameters` | No | List of `{"name": str, "type": str, "label": str, "default": Any}`. Each generates a labeled input. Type can be `"string"`, `"integer"`, `"number"`, or `"date"`. |
| `outputs` | No | List of destination type strings, shown in a dropdown on the source screen. |

---

## Credential Storage

Credentials are stored in `~/.hermes/credentials.json` (JSON, plaintext).  
Saved in the format `{"source_id": {"key": "value", ...}}`.

The Credentials screen shows a three-level hierarchy matching Data Sources.  
You can pre-fill credentials for any source that has `credentials` defined in its metadata.

---

## Dynamic Pages — How It Works

The TUI never hardcodes source-specific forms.

| Auth type | How it's handled |
|---|---|
| **API Key** | Add `{"key": "api_key", "label": "API Key"}` to `credentials`. Renders a password-masked input. |
| **Token** | Same pattern — `{"key": "token", "label": "Bearer Token"}`. |
| **Email + Password** | Add two entries to `credentials`. Both render as inputs (password-masked). |
| **OAuth** | Not yet supported (future). For now, store the refresh token as a credential. |
| **No auth** | Omit `credentials` entirely. The credential step is skipped. |

The SourceScreen checks `metadata()` output at compose time:
- Has `credentials` → show credential status indicators (✓/✗)
- Has `parameters` → render `ParameterForm` dynamically
- Has `outputs` → render `DestinationSelector` dropdown
- None of the above → show "not implemented yet" message

When none of `credentials`/`parameters`/`outputs` are present, the TUI knows it's a catalog stub and shows an informational message instead of a form.
