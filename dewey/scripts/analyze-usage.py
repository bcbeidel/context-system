#!/usr/bin/env python3
"""Analyze context usage and generate token inventory.

This script scans a context directory and generates:
- Token inventory CSV
- Summary report
- Baseline measurements
"""

import csv
import sys
from pathlib import Path

import click

# Add src to path so we can import dewey
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dewey.core.measurement.token_counter import (
    format_summary,
    scan_directory,
)


@click.command()
@click.option(
    "--directory",
    "-d",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Directory to scan (default: ./context or current directory)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Output CSV file (default: ~/.claude/analytics/context-inventory.csv)",
)
@click.option(
    "--extensions",
    "-e",
    multiple=True,
    help="File extensions to include (e.g., -e .md -e .txt)",
)
@click.option(
    "--report",
    "-r",
    is_flag=True,
    help="Generate summary report",
)
@click.option(
    "--baseline",
    "-b",
    is_flag=True,
    help="Save baseline report to ~/.claude/analytics/baseline.txt",
)
def main(
    directory: Path,
    output: Path,
    extensions: tuple,
    report: bool,
    baseline: bool,
) -> None:
    """Analyze context usage and generate token inventory.

    Examples:

        # Scan context directory and save inventory
        python analyze-usage.py -d context -o inventory.csv

        # Generate baseline report
        python analyze-usage.py -d context --baseline

        # Show summary report
        python analyze-usage.py -d context --report
    """
    # Set defaults
    if directory is None:
        # Try common locations
        if Path("context").exists():
            directory = Path("context")
        else:
            directory = Path.cwd()

    if output is None:
        output = Path.home() / ".claude" / "analytics" / "context-inventory.csv"

    # Convert extensions tuple to list
    ext_list = list(extensions) if extensions else None

    click.echo(f"Scanning directory: {directory}")

    try:
        results = scan_directory(directory, extensions=ext_list)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if not results:
        click.echo("No files found matching criteria.")
        sys.exit(0)

    click.echo(f"Found {len(results)} files")

    # Ensure output directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    # Write CSV
    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["file", "tokens", "lines", "bytes", "absolute_path"]
        )
        writer.writeheader()
        writer.writerows(results)

    click.echo(f"Wrote inventory to: {output}")

    # Generate summary report
    if report or baseline:
        summary = format_summary(results)
        click.echo("\n" + summary)

    # Save baseline report
    if baseline:
        baseline_path = (
            Path.home() / ".claude" / "analytics" / "baseline.txt"
        )
        baseline_path.parent.mkdir(parents=True, exist_ok=True)

        with open(baseline_path, "w") as f:
            f.write(summary)

        click.echo(f"\nBaseline report saved to: {baseline_path}")


if __name__ == "__main__":
    main()
