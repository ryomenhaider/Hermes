import dataclasses
import json
import sys


def _profile(argv: list[str]) -> int:
    from hermes.api.data import profile

    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]
    if not paths:
        print("hermes: 'profile' requires at least one file path", file=sys.stderr)
        return 2

    code = 0
    for path in paths:
        try:
            md = profile(path=path, source=path)
            if as_json:
                print(json.dumps(dataclasses.asdict(md), default=str))
            else:
                print(_render(md))
        except Exception as e:  # noqa: BLE001 - CLI boundary
            print(f"hermes: {e}", file=sys.stderr)
            code = 1
    return code


def _fmt(value: object) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def _render(md: object) -> str:
    import polars as pl

    from hermes.core.metadata import MetaData

    assert isinstance(md, MetaData)
    deep = md.deep_stats
    lines = [
        f"Profile: {md.source or 'dataset'}",
        f"Rows: {md.row_count:,}  Columns: {md.column_count}  "
        f"Duplicates: {md.quality.duplicate_count if md.quality else 0}"
        f"  Deep stats: {'yes' if deep else 'no (rows > 5,000,000)'}",
    ]
    if md.date_range:
        col = next(iter(md.date_range))
        lo, hi = md.date_range[col]
        lines.append(f"Date range: {col} {_fmt(lo)} .. {_fmt(hi)}")
    if md.frequency:
        lines.append(f"Frequency: {md.frequency}")

    rows = {
        "column": [c.name for c in md.columns],
        "dtype": [c.dtype for c in md.columns],
        "nulls": [str(c.null_count) for c in md.columns],
        "null%": [f"{c.null_ratio * 100:.2f}" for c in md.columns],
        "unique": [str(c.unique_count) if deep else "-" for c in md.columns],
        "min": [_fmt(c.min_value) for c in md.columns],
        "max": [_fmt(c.max_value) for c in md.columns],
        "mean": [_fmt(c.mean) for c in md.columns],
        "std": [_fmt(c.std) for c in md.columns],
        "top 5": [
            ", ".join(f"{key!s}x{count}" for key, count in c.top_values[:5]) if c.top_values else "-"
            for c in md.columns
        ],
    }
    return "\n".join([*lines, "", str(pl.DataFrame(rows))])


def app():
    argv = sys.argv[1:]

    if argv and argv[0] == "profile":
        raise SystemExit(_profile(argv[1:]))

    import hermes._rust as _rust

    raise SystemExit(_rust.cli.main(argv))


if __name__ == "__main__":
    app()