import logging
import time
from pathlib import Path

import polars as pl

logger = logging.getLogger(__name__)


def export(data: pl.DataFrame, filetype: str = "csv", loc: Path | str = "data/", name: str | None = None) -> Path:

    if not isinstance(data, pl.DataFrame):
        raise TypeError(f"The data should be a polars DataFrame, got {type(data)}")

    filetype = filetype.lower()
    file_name = f"{name}.{filetype}" if name else f"{round(time.time())}.{filetype}"

    target_dir = Path(loc)
    target_dir.mkdir(parents=True, exist_ok=True)
    full_path = target_dir / file_name

    if filetype == "csv":
        data.write_csv(full_path)
    elif filetype == "json":
        data.write_json(full_path)
    elif filetype == "parquet":
        data.write_parquet(full_path)
    else:
        raise ValueError(f"Unsupported export format {filetype!r}; expected csv, json, or parquet")

    logger.info("Successfully exported data to %s", full_path)
    return full_path


if __name__ == "__main__":
    df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie", "Diana"],
            "Age": [32, 32, 22, 43],
            "City": ["New York", "London", "Paris", "Tokyo"],
            "Salary": [70000, 85000, 95000, 80000],
        }
    )

    export(data=df, filetype="csv", name="demo")