import argparse
import dataclasses
import json
import sys
from pathlib import Path


def _fmt(value: object) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def _render_profile(md: object) -> str:
    import polars as pl

    from hermes.core.metadata import MetaData

    assert isinstance(md, MetaData)
    rows = {
        "column": [c.name for c in md.columns],
        "dtype": [c.dtype for c in md.columns],
        "nulls": [str(c.null_count) for c in md.columns],
        "null%": [f"{c.null_ratio * 100:.2f}" for c in md.columns],
        "unique": [str(c.unique_count) if md.deep_stats else "-" for c in md.columns],
        "min": [_fmt(c.min_value) for c in md.columns],
        "max": [_fmt(c.max_value) for c in md.columns],
        "mean": [_fmt(c.mean) for c in md.columns],
        "std": [_fmt(c.std) for c in md.columns],
        "top 5": [
            ", ".join(f"{key!s}x{count}" for key, count in c.top_values[:5]) if c.top_values else "-"
            for c in md.columns
        ],
    }
    lines = [
        f"Profile: {md.source or 'dataset'}",
        f"Rows: {md.row_count:,}  Columns: {md.column_count}  "
        f"Duplicates: {md.quality.duplicate_count if md.quality else 0}"
        f"  Deep stats: {'yes' if md.deep_stats else 'no (rows > 5,000,000)'}",
    ]
    if md.date_range:
        col = next(iter(md.date_range))
        lo, hi = md.date_range[col]
        lines.append(f"Date range: {col} {_fmt(lo)} .. {_fmt(hi)}")
    if md.frequency:
        lines.append(f"Frequency: {md.frequency}")
    return "\n".join([*lines, "", str(pl.DataFrame(rows))])


def _loaded(name: str):
    import hermes as hr

    path = Path(name)
    if path.is_file():
        return hr.ingest(path)
    result = hr.load(name)
    if not result.is_success():
        raise hr.HermesError(str(result.errors[0]))
    return result.data


def _profile(args: argparse.Namespace) -> int:
    import hermes as hr

    path = Path(args.name)
    md = hr.profile(path=path) if path.is_file() else hr.profile(data=_loaded(args.name), source=args.name)
    if args.json:
        print(json.dumps(dataclasses.asdict(md), default=str))
    else:
        print(_render_profile(md))
    return 0


def _fail(action: str, error: object) -> int:
    print(f"hermes: {action}: {error}", file=sys.stderr)
    return 1


def _fetch(args: argparse.Namespace) -> int:
    import hermes as hr

    kwargs = {"dataset": args.dataset} if args.dataset else {}
    try:
        ds = hr.ingest(args.source, **kwargs)
    except hr.HermesError as e:
        return _fail("fetch", e)
    try:
        print(f"Fetched {ds.name} ({ds.to_polars().height:,} rows, {ds.to_polars().width} cols)")
    except Exception as e:  # noqa: BLE001
        return _fail("fetch", e)
    return 0


def _inspect(args: argparse.Namespace) -> int:
    import hermes as hr

    report = hr.inspect(_loaded(args.name))
    print(f"Inspect: {args.name}  rows: {report.row_count:,}  cols: {report.column_count}  needs: {report.needs or '-'}")
    return 0


def _entity(args: argparse.Namespace) -> int:
    import hermes as hr

    result = hr.resolve_entity(args.query, entity_type=args.type)
    if not result.is_success():
        return _fail("entity resolve", result.errors[0] if result.errors else "no match")
    entity = result.data
    print(f"{entity.entity_type}: {entity.canonical_name}  ({entity.id})")
    if entity.country_id:
        print(f"  country: {entity.country_id}")
    for key in entity.identifiers:
        print(f"  {key}: {entity.identifiers[key].value}")
    return 0


def _dataset(args: argparse.Namespace) -> int:
    import hermes as hr

    if args.action == "list":
        if not hr.list_datasets().is_success():
            print("(no datasets)", file=sys.stderr)
            return 1
        for name in hr.list_datasets().data:
            print(name)
        return 0
    result = hr.storage_info(args.name) if args.action == "info" else hr.delete(args.name)
    if not result.is_success():
        return _fail(f"dataset {args.action}", result.error)
    if args.action == "delete":
        print(f"deleted {args.name}")
        return 0
    info = result.data
    print(
        f"dataset: {info.dataset}  rows: {info.rows}  cols: {info.columns}  "
        f"size: {info.size:,} B  version: {info.version}  format: {info.format}"
    )
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hermes", description="Hermes data engine")
    parser.add_argument("--version", action="version", version="hermes 0.1")
    sub = parser.add_subparsers(dest="command")

    p_fetch = sub.add_parser("fetch", help="Fetch data from a connector or local file")
    p_fetch.add_argument("source", help="connector name ('public_data', 'binance', ...) or file path")
    p_fetch.add_argument("dataset", nargs="?", help="dataset id for connectors")
    p_fetch.set_defaults(func=_fetch)

    p_inspect = sub.add_parser("inspect", help="Inspect data for entity needs and issues")
    p_inspect.add_argument("name", help="file path or stored dataset name")
    p_inspect.set_defaults(func=_inspect)

    p_profile = sub.add_parser("profile", help="Profile data as a table of column stats")
    p_profile.add_argument("name", help="file path or stored dataset name")
    p_profile.add_argument("--json", action="store_true", help="emit JSON")
    p_profile.set_defaults(func=_profile)

    p_entity = sub.add_parser("entity", help="Work with entities")
    e_sub = p_entity.add_subparsers(dest="action", required=True)
    p_resolve = e_sub.add_parser("resolve", help="Resolve a name/identifier to an entity")
    p_resolve.add_argument("query", help="canonical name or identifier value")
    p_resolve.add_argument("--type", default=None, help="hint entity type (company, country, security, ...)")
    p_resolve.set_defaults(func=_entity)

    p_dataset = sub.add_parser("dataset", help="Manage stored datasets")
    d_sub = p_dataset.add_subparsers(dest="action", required=True)
    p_list = d_sub.add_parser("list", help="List stored datasets")
    p_list.set_defaults(func=_dataset)
    p_info = d_sub.add_parser("info", help="Show info about a stored dataset")
    p_info.add_argument("name")
    p_info.set_defaults(func=_dataset)
    p_delete = d_sub.add_parser("delete", help="Delete a stored dataset")
    p_delete.add_argument("name")
    p_delete.set_defaults(func=_dataset)

    return parser


def app() -> None:
    from hermes.core.errors import HermesError

    parser = _build_parser()
    args = parser.parse_args()
    if not getattr(args, "func", None):
        parser.print_help(sys.stdout)
        raise SystemExit(0)
    try:
        raise SystemExit(args.func(args))
    except HermesError as e:
        raise SystemExit(_fail("error", e))
    except Exception as e:  # noqa: BLE001 - CLI boundary
        raise SystemExit(_fail("error", e))


def _fail(action: str, error: object) -> int:
    print(f"hermes: {action}: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    app()