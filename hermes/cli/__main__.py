from pathlib import Path

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from hermes.api.data import profile

app = typer.Typer(
    name="hermes",
    help="Foundational intelligence data platform.",
    no_args_is_help=True,
)


@app.command()
def version():
    typer.echo("Hermes v0.2.16")


@app.command()
def info():
    typer.echo("Hermes v0.2.16")
    typer.echo("Foundational intelligence data platform")

@app.command()
def profile_data(
    path: Path = typer.Argument(
        help="Path to the dataset.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
):

    report = profile(path=path)

    def fmt(value):
        if value is None:
            return "—"
        if isinstance(value, float):
            return f"{value:.4g}"
        return str(value)

    date_range = "n/a"
    if report.date_range:
        ranges = report.date_range if isinstance(report.date_range, list) else [report.date_range]
        date_range = ", ".join(
            f"{col}: {lo} → {hi}"
            for rng in ranges
            if rng
            for col, (lo, hi) in rng.items()
        )

    frequency = "n/a"
    if report.frequency:
        frequency = ", ".join(str(f) for f in report.frequency)

    retrieved = report.retrieved_at.strftime("%Y-%m-%d %H:%M:%S %Z") if report.retrieved_at else "n/a"

    summary = Table(show_header=False, box=None, padding=(0, 2))
    summary.add_column(style="bold cyan", justify="right")
    labels = [
        ("File", str(path)),
        ("Rows", f"{report.row_count:,}"),
        ("Columns", str(report.column_count)),
        ("Date range", date_range),
        ("Frequency", frequency),
        ("Retrieved", retrieved),
    ]
    if report.source:
        labels.insert(2, ("Source", report.source))
    for label, value in labels:
        summary.add_row(label, value)

    columns = Table(header_style="bold cyan", box=box.SIMPLE_HEAVY)
    columns.add_column("Column", style="bold", no_wrap=True)
    columns.add_column("Type")
    columns.add_column("Unique", justify="right")
    columns.add_column("Nulls", justify="right")
    columns.add_column("Null%", justify="right")
    columns.add_column("Min", justify="right")
    columns.add_column("Max", justify="right")
    columns.add_column("Mean", justify="right")
    columns.add_column("Median", justify="right")

    for col in report.columns:
        columns.add_row(
            col.name,
            col.dtype,
            str(col.unique_count),
            str(col.null_count),
            f"{col.null_ratio:.2%}",
            fmt(col.min_value),
            fmt(col.max_value),
            fmt(col.mean),
            fmt(col.median),
        )

    top_values = Table(show_header=False, box=None, padding=(0, 2))
    top_values.add_column(style="bold", no_wrap=True)
    top_values.add_column()
    for col in report.columns:
        if col.top_values:
            top_values.add_row(
                col.name,
                ", ".join(f"{k} ({v})" for k, v in col.top_values[:5]),
            )

    body = [
        Panel(summary, title="[bold]Profile Report[/bold]", border_style="cyan"),
        Panel(columns, title="[bold]Columns[/bold]", border_style="cyan"),
    ]
    if top_values.rows:
        body.append(Panel(top_values, title="[bold]Top Values[/bold]", border_style="cyan"))

    quality = report.quality
    if quality:
        completeness = quality.completeness or {}
        incomplete = {k: v for k, v in completeness.items() if v < 1.0}
        if incomplete:
            comp = ", ".join(f"{k} {v:.2%}" for k, v in incomplete.items())
        else:
            comp = "100% (all columns complete)"

        anomalies = {k: v for k, v in (quality.anomaly_count or {}).items() if v > 0}
        if anomalies:
            anom = ", ".join(f"{k}: {v}" for k, v in anomalies.items())
        else:
            anom = "none detected"

        q = Table(show_header=False, box=None, padding=(0, 2))
        q.add_column(style="bold cyan", justify="right")
        q.add_row("Completeness", comp)
        q.add_row("Duplicates", str(quality.duplicate_count))
        q.add_row("Anomalies", anom)
        body.append(Panel(q, title="[bold]Quality[/bold]", border_style="cyan"))

    console = Console(soft_wrap=True)
    for renderable in body:
        console.print(renderable)

if __name__ == "__main__":
    app()
