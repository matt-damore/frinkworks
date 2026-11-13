import json
import subprocess
from pathlib import Path
from typing import Any


class MediaInfoError(Exception):
    """Raise when MediaInfo metadata extraction fails."""


def extract_metadata(file_path: str | Path) -> dict[str, Any]:
    """Extract technical media metadata using MediaInfo CLI."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Media file not found: {path}")

    try:
        result = subprocess.run(
            ["mediainfo", "--Output=JSON", str(path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            timeout=60,
        )
    except FileNotFoundError as exc:
        raise MediaInfoError(
            "MediaInfo CLI was not found. Ensure it is installed and available on PATH."
        ) from exc

    except subprocess.TimeoutExpired as exc:
        raise MediaInfoError(f"MediaInfo timed out while processing: {path}") from exc

    except subprocess.CalledProcessError as exc:
        raise MediaInfoError(f"MediaInfo failed to process {path}: {exc.stderr}") from exc

    try:
        metadata = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise MediaInfoError(f"MediaInfo returned invalid JSON for {path}") from exc

    if not isinstance(metadata, dict):
        raise MediaInfoError(f"MediaInfo returned an unexpected JSON structure for {path}")

    return metadata
