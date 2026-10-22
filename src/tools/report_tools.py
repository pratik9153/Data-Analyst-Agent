
"""Report export tools."""

from pathlib import Path
from datetime import datetime


def export_markdown_report(
    title: str,
    content: str,
    output_dir: str = "reports",
    filename: str | None = None,
) -> dict:
    # Create the output directory if it does not exist
    report_dir = Path(output_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    # Create a filename when one is not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_report_{timestamp}.md"

    # Make sure the filename is safe and uses Markdown format
    report_name = Path(filename).name

    if not report_name.lower().endswith(".md"):
        report_name += ".md"

    report_path = report_dir / report_name

    # Build the report content
    report_text = (
        f"# {title}\n\n"
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"{content.strip()}\n"
    )

    # Save the report as a Markdown file
    report_path.write_text(report_text, encoding="utf-8")

    # Return information about the saved report
    return {
        "success": True,
        "report_path": str(report_path),
        "file_size_bytes": report_path.stat().st_size,
    }
